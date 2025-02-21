import logging
import os
import json

import requests as _requests
from tqdm import tqdm

from lm_eval.api.model import LM
from lm_eval.api.registry import register_model
from lm_eval.models.utils import retry_on_specific_exceptions
import time

logger = logging.getLogger(__name__)


def together_completion(**kwargs):
    """Query Together API for completion.
    Retry with back-off until they respond.
    """

    def _exception_callback(e: Exception, sleep_time: float) -> None:
        import traceback

        traceback.print_exc()

    @retry_on_specific_exceptions(
        on_exceptions=[_requests.exceptions.RequestException],
        max_retries=None,  # retry forever, consider changing
        on_exception_callback=_exception_callback,
    )
    def completion():
        return _requests.post(**kwargs)

    return completion()


@register_model("together")
class TogetherLM(LM):
    def __init__(self, model, truncate: bool = False, check_completion : bool = False, **kwargs) -> None:
        """
        :param model: str
            Together API model
        :param truncate: bool
            Truncate input if too long (if False and input is too long, throw error)
        """
        super().__init__()

        self.model = model
        self.truncate = truncate
        self.api_url = "https://api.together.xyz"
        # Read from environment variable
        self.api_key = os.environ["TOGETHER_API_KEY"]
        self.check_completion = check_completion
        self.history = dict()        

    @property
    def eot_token_id(self):
        # Isn't used because we override loglikelihood, loglikelihood_rolling and generate_until
        raise NotImplementedError()

    @property
    def max_length(self) -> int:
        # NOTE: Turn on truncation to avoid errors on long inputs.
        return 4096

    @property
    def max_gen_toks(self) -> int:
        return 256

    @property
    def batch_size(self):
        # Isn't used because we override loglikelihood, loglikelihood_rolling and generate_until
        raise NotImplementedError()

    @property
    def device(self):
        # Isn't used because we override loglikelihood, loglikelihood_rolling and generate_until
        raise NotImplementedError()

    def tok_encode(self, string: str):
        # Isn't used because we override loglikelihood, loglikelihood_rolling and generate_until
        raise NotImplementedError()

    def tok_decode(self, tokens):
        # Isn't used because we override loglikelihood, loglikelihood_rolling and generate_until
        raise NotImplementedError()

    def loglikelihood(self, requests, disable_tqdm: bool = False):
        res = []
        for context, continuation in tqdm([req.args for req in requests], disable=disable_tqdm):
            for i in range(100): # We do 100 retries for each request to ensure we get a response
                # to obtain the logprobs of the continuation, we first get the logprobs of the context + continuation
                response = together_completion(
                    url=self.api_url + "/v1/completions/",
                    headers={"Authorization": "Bearer " + self.api_key},
                    json={"prompt": context + continuation, "model": self.model, "logprobs": 1, 'echo': True, "max_tokens": 1},
                )
                
                try:
                    # We then get the logprobs of the context alone, so we can subtract it from the context + continuation logprobs
                    if context not in self.history:
                        response_prompt_alone = together_completion(
                            url=self.api_url + "/v1/completions/",
                            headers={"Authorization": "Bearer " + self.api_key},
                            json={"prompt": context, "model": self.model, "logprobs": 1, 'echo': True, "max_tokens": 1},
                        )
                        resp_prompt_alone = response_prompt_alone.json()
                        logprob_prompt = sum(resp_prompt_alone['prompt'][0]['logprobs']["token_logprobs"][1:])
                        self.history[context] = logprob_prompt
                    else:
                        logprob_prompt = self.history[context]

                    # We check if the completion by the model is correct, this needs a separate call
                    correct = False
                    if self.check_completion:
                        response_completion = together_completion(
                            url=self.api_url + "/v1/completions/",
                            headers={"Authorization": "Bearer " + self.api_key},
                            json={"prompt": context, "model": self.model, "logprobs": 1, 'echo': True, "max_tokens": 10, "temperature": 0, "top_k": 1},
                        )
                        resp_completion = response_completion.json()
                        s = resp_completion["choices"][0]['text']
                        correct = continuation.startswith(s) or s.startswith(continuation)

                    resp = response.json()
                    logprob = sum(resp['prompt'][0]['logprobs']["token_logprobs"][1:]) - logprob_prompt
                    res.append((logprob, correct))
                    self.cache_hook.add_partial(
                        "loglikelihood", (context, continuation), (logprob, correct)
                    )
                    break
                except Exception as e:
                    logger.error(f'Error Occurred: {e} for response {response}')
                if i == 99:
                    assert False
        return res

    def loglikelihood_rolling(self, requests, disable_tqdm: bool = False):
        # TODO: The Together API does not support tokenized inputs so we cannot
        # manually partition long contexts into smaller rolling windows as
        # done for other models derived from `BaseLM`. Override this method
        # with a windowing scheme that works for direct string inputs.
        raise NotImplementedError(
            "`loglikelihood_rolling` is currently not supported due to lack of "
            "input tokenization support from Together."
        )

    def generate_until(self, requests, disable_tqdm: bool = False):
        if not requests:
            return []

        res = []
        for request in tqdm(requests, disable=disable_tqdm):
            for i in range(100):
                inp = request.arguments[0]
                request_args = request.arguments[1]
                until = request_args["until"]
                response = together_completion(
                    url=self.api_url + "/v1/completions/",
                    headers={"Authorization": "Bearer " + self.api_key},
                    json={
                        "prompt": inp,
                        "max_tokens": self.max_gen_toks,
                        "top_k": 1,
                        "stop": until,
                        "model": self.model
                    },
                )
                try:
                    resp = response.json()
                    s = resp["choices"][0]['text']
                    res.append(s)

                    self.cache_hook.add_partial("generate_until", (inp, request_args), s)
                    break
                except Exception as e:
                    logger.error(f'Error Occurred: {e} for response {response}')
                if i == 99:
                    assert False
        return res

    def _model_call(self, inps):
        # Isn't used because we override _loglikelihood_tokens
        raise NotImplementedError()

    def _model_generate(self, context, max_length, eos_token_id):
        # Isn't used because we override generate_until
        raise NotImplementedError()