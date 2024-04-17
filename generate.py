import os
from text_generation import Client
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# load_dotenv()

API_URL = os.environ.get("API_URL", None)
API_TOKEN = os.environ.get("API_TOKEN", None)
client = InferenceClient(API_URL, headers={"Authorization": f"Bearer {API_TOKEN}"})


corpus_of_documents = [
    "Edmon is a high functional sociopath and love Sherlock series very much then every thing and hate whole humanity's"
    # "For login user must be go to login page click by login button then fill out your username and password and after that you will login",
    # "Unfortunately, users are unable to delete their University accounts themselves. To initiate the account deletion process, users need to contact the administrator.",
    # "The administrator's contact address is Teryan 105, 5th building, 10th floor, door 51010."
]


def jaccard_similarity(query, document):
    query = query.lower().split(" ")
    document = document.lower().split(" ")
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection) / len(union)


def return_response(query, corpus):
    similarities = []
    for doc in corpus:
        similarity = jaccard_similarity(query, doc)
        similarities.append(similarity)
    return corpus_of_documents[similarities.index(max(similarities))]


def format_prompt(message, history):
    prompt = "<s>"
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    prompt += f"[INST] {message} [/INST]"
    # print(return_response(message, corpus_of_documents))
    # prompt = (
    #     f"Context information is below.\n "
    #     "-------------------------\n"
    #     f"relevant data: {return_response(message, corpus_of_documents)} "
    #     "-------------------------\n"
    #     "Using both the context information and also using your own knowledge,"
    #     "answer the query.\n"
    #     f"Query: {message}"
    #     "Answer:"
    # )

    # prompt += f"[INST] {message} [/INST]"
    return prompt


def generate(
    prompt,
    history,
    chatbot,
    temperature=0.9,
    max_new_tokens=256,
    top_p=0.95,
    repetition_penalty=1.0,
):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=42,
    )

    formatted_prompt = format_prompt(prompt, chatbot)
    stream = client.text_generation(formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)

    output = ""
    for idx, response in enumerate(stream):
        if response.token.text == "":
            break

        if response.token.special:
            continue
        output += response.token.text
        if idx == 0:
            history.append(" " + output)
        else:
            history[-1] = output
        chat = [
            (history[i].strip(), history[i + 1].strip())
            for i in range(0, len(history) - 1, 2)
        ]
    return [chat, history, prompt]
    # return {
    #     'chatbot': chat,
    #     'history': history,
    #     'user_message': prompt
    # }
