from typing import Final
import litellm
from litellm import Router

MODEL_LIST: Final = [
    {
        "model_name": "production-gpt",
        "litellm_params": {
            "model": "gpt-4o",
            "mock_response": "Response from Deployment 1 (US East)",
            "rpm": 100,
        },
    },
    {
        "model_name": "production-gpt",
        "litellm_params": {
            "model": "azure/gpt-4o",
            "mock_response": "Response from Deployment 2 (EU West)",
            "rpm": 100,
        },
    },
    {
        "model_name": "fallback-claude",
        "litellm_params": {
            "model": "anthropic/claude-3-5-sonnet-20241022",
            "mock_response": "Response from Fallback Deployment (Anthropic)",
        },
    },
]

router: Final = Router(
    model_list=MODEL_LIST,
    routing_strategy="least-busy",
    fallbacks=[{"production-gpt": ["fallback-claude"]}],
    num_retries=2,
    cooldown_time=30,
)


def run_load_balancing_demo() -> None:
    print("--- Demonstrating Router Load Balancing (least-busy) ---")
    messages: Final = [{"role": "user", "content": "Hello from LiteLLM Router"}]
    for i in range(4):
        response: Final = router.completion(model="production-gpt", messages=messages)
        print(f"Request {i + 1}: {response.choices[0].message.content}")


if __name__ == "__main__":
    run_load_balancing_demo()
