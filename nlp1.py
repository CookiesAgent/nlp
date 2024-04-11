from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel, GPT2TokenizerFast, GPT2Tokenizer
import syllables
import torch

def load_model(model_path):
    model = GPT2LMHeadModel.from_pretrained(model_path)
    return model


def load_tokenizer(tokenizer_path):
    tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
    return tokenizer

model_path = "D:/nlp_poetry"
max_len = 50
model = load_model(model_path)
tokenizer = load_tokenizer(model_path)

correctNumSyl=[]
perps=[]

f=open('poetry_results.txt', 'a', encoding="utf8")

def generate_text(model_path, sequence, max_length):
    ids = tokenizer.encode(f'{sequence}', return_tensors='pt')
    final_outputs = model.generate(
        ids,
        do_sample=True,
        max_length=max_length,
        pad_token_id=model.config.eos_token_id,
        top_k=50,
        top_p=0.95,
    )
    output=tokenizer.decode(final_outputs[0], skip_special_tokens=True)
    return output

def rhyme(line, rhyme_syl):
    syl=syllables.estimate(line)
    if syl<(rhyme_syl-1) or syl>(rhyme_syl+1):
        return False
    else:
        return True

def avg_syl(sequence):
    total=0
    numLines=0
    lines=sequence.splitlines()
    for line in lines:
        if line!="":
            total=total+syllables.estimate(line)
            numLines=numLines+1
    return total/numLines


def perp(line):
    inputs = tokenizer(line, return_tensors = "pt")

    loss = model(input_ids = inputs["input_ids"], labels = inputs["input_ids"]).loss

    ppl = torch.exp(loss)
    return ppl.item()

def generate_poetry(sequence):
    f.write("\nThe input:\n"+sequence)
    f.write("\nThe next line:\n")
    if not sequence.endswith("\n"):
        sequence=sequence+"\n"
    syl=avg_syl(sequence)
    l=len(sequence)
    r=False
    i=0
    while(not r and i<=5):
        text=generate_text(model_path, sequence, max_len)
        text=text[slice(l, None, 1)]
        i=i+1
        lines=text.splitlines()
        final_line="None"
        if len(lines)>0:
            final_line=lines[0]
        if final_line=="" or final_line=="\n":
            final_line=lines[1] 

        r=rhyme(final_line, syl)

    f.write(final_line)
    perplexity=perp(final_line)

    perps.append(perplexity)

    correctNumSyl.append(r)

    f.write("\nPerplexity: "+str(perplexity))
    f.write("\nAvg. number of syllables in the input lines: "+str(syl))
    f.write("\nNumber of syllables in the generetad line: "+str(syllables.estimate(final_line)))
    f.write("\n============================")
    return final_line


def get_test(file_path):
    sequences = []
    with open(file_path, 'r', encoding="utf8") as file:
        chunk = ""
        for line in file:
            if line.strip() == "~":
                sequences.append(chunk.strip())
                chunk = ""
            else:
                chunk += line
        # Append the last chunk
        if chunk:
            sequences.append(chunk.strip())
    return sequences


def calculate_percentage_of_true(binary_list):
    if not binary_list:
        return 0.0  # Return 0 if the list is empty
    true_count = sum(binary_list)
    return (true_count / len(binary_list)) * 100





file_path = 'gutenberg_crash.txt' 
sequences = get_test(file_path)

# Call func1 on each chunk
for sequence in sequences:
    generate_poetry(sequence)
percentage_true = calculate_percentage_of_true(correctNumSyl)
avg_perp= sum(perps) / len(perps)

f.write("\n\n\n==================")
f.write("\nPercentage of times when number of syllables matched: "+str(percentage_true))
f.write("\nAverage perplexity of the model: "+str(avg_perp))
f.write("\n==================")
f.close()