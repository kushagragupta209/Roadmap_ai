import os
from dotenv import load_dotenv
from groq import Groq
from reAct_prompt.reAct import llama_reAct

load_dotenv(dotenv_path="env/.env")

client = Groq(api_key=os.getenv("groq_llama_key"))

query = "Give me the roadmap for preparing for the GATE 2026 DA exam."
syllabus = "Probability and Statistics: Counting (permutation and combinations), probability axioms,Sample space, events, independent events, mutually exclusive events, marginal,conditional and joint probability, Bayes Theorem, conditional expectation and variance,mean, median, mode and standard deviation, correlation, and covariance, randomvariables, discrete random variables and probability mass functions, uniform, Bernoulli,binomial distribution, Continuous random variables and probability distribution function,uniform, exponential, Poisson, normal, standard normal, t-distribution, chi-squareddistributions, cumulative distribution function, Conditional PDF, Central limit theorem,confidence interval, z-test, t-test, chi-squared test."

def model_call():

    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            # {
            #     "role": "system",
            #     "content": llama_reAct()
            # },
            {
                "role": "system",
                "content": llama_reAct(query, syllabus)
            }
        ]
    )
    # print(completion.choices[0].message.content)
    raw_output = completion.choices[0].message.content
    # print(f"RAW OUTPUT - {raw_output}")


    # if "Answer" in raw_output:
    #     final_answer = raw_output.split("```json")[1].split()
    # else:
    #     final_answer = raw_output
    # print("final_answer - ", final_answer)

    import json 
    data={}
    if "Final Answer:" in raw_output:
        json_index = raw_output.index("Final Answer:")
        json_code = raw_output[json_index:]
        json_str = json_code.split("Final Answer:")[1].strip()
        data = json.loads(json_str)
        return data
        print(data)
    else:
        print("No json result found")

    # if mermaid_code:
    #     mermaid_code = "".join(mermaid_code)
    #     mermaid_code = mermaid_code.replace("\n", "")
    #     mermaid_code = mermaid_code.replace(";", ";\n")
        # print(mermaid_code)

    return data
# model_call()
