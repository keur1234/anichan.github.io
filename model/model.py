import pathlib
import os
import pandas as pd
import numpy as np
from nltk import edit_distance


ANIME_CLASSES_PATH = pathlib.Path(__file__).parent.parent / "data-sets\Anime_classes.csv"
ANIME_NAMES_PATH = pathlib.Path(__file__).parent.parent / "data-sets\Anime_names.csv"
ANIME_SCORE_PATH = pathlib.Path(__file__).parent.parent / "data-sets\Anime_score.csv"

anime_classes = pd.read_csv(ANIME_CLASSES_PATH, index_col=0)
anime_names = pd.read_csv(ANIME_NAMES_PATH, index_col=0)
anime_score = pd.read_csv(ANIME_SCORE_PATH, index_col=0)
classes = anime_classes.columns

## wrapper function for debugging
def timeit(func):
    from time import time
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"Time taken: {end - start} sec.")
        return result
    return wrapper

def inf_loops(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                print(func(*args, **kwargs))
            except Exception as e:
                print(e)
    return wrapper

def input_test(func, _prompt= "Enter your input: "):
    def wrapper(*args, **kwargs):
        str = input(_prompt)
        out = func(str)
        return out
    return wrapper
### ------------------

def tokenizer(input:str, sep:str=" "):
    """
    return list of string from input string seperated by sep
    """
    list = input.split(sep)

    # #remove space in last and first.
    list = [ ele.strip() for ele in list]

    return list


def vectorize_classes(inp_classes:list):
    """
    vectorize the classes to be used in predict function
    if input not in classes, it will be ignored.
    inputs classes: list of string of anime classes. such as ["Action", "Adventure", "Comedy"]
    return: vectorized classes contain value (0 or 1), length=len(anime_classes.columns)
    """
    similarlity_scores = np.vectorize(similarlity_score)

    vectorize = np.zeros(len(classes),dtype=np.uint8)
    for inp in inp_classes:
        sim = similarlity_scores(inp, classes, 6)
        if not np.all(sim == 0):
            id = np.argmax(sim)
            vectorize[id] = 1
    return vectorize


# model
def predict(predict_classes:np.ndarray, n:int=5, return_only_titles:bool=False):
    """
    predicts the anime name based on the classes using cosine similarity
    inputs predict_classes: vectorized classes contain value (0 or 1), length=len(anime_classes.columns)
            n: length of output to return. if n=-1, return all
    return: if return_only_titles=false return dictionary of anime names, id and similarity score, length=n sorted by similarity score(reverted order).
            else return list of anime names length=n sorted by similarity score(reverted order).
    """

    # apply Cosine Similarity.
    similarity = {
        "id" : anime_classes.index,
        "value" : np.dot(anime_classes.values, predict_classes) / np.linalg.norm(anime_classes.values) * np.linalg.norm(predict_classes)
    }

    #sort similarity with reverted order.
    similarity["value"] = similarity["value"] * anime_score["score"] / 10
    similarity["id"] = np.argsort(similarity["value"])[::-1] + 1
    similarity["value"] = np.sort(similarity["value"])[::-1]

    #select top n value.
    if n != -1:
        similarity["id"] =  similarity["id"][:n]
        similarity["value"] =  similarity["value"][:n]

    #get title of anime.
    title = anime_names["title"].loc[similarity["id"]].values

    if return_only_titles:
        return title

    else:
        return {
            "title" : title,
            "id" : similarity["id"],
            "similarity" : similarity["value"]
        }


def similarlity_score(a:str, b:str, cut_out=20):
    """
    return similarlity_score of string a, b
    range between 0 and 1
    cut_out: if edit_distance > cut_out, return 0
    """
    distance = edit_distance(a.capitalize(), b.capitalize())
    similarlity_score = 1 - (distance / cut_out) if distance < cut_out else 0
    return similarlity_score


def get_anime_id_by_name(name:str):
    """
    get anime id which anime name is most similar to input name.'''''''''''
    """
    similarlity_scores = np.vectorize(similarlity_score)
    sim_scores = similarlity_scores(name, anime_names["title"])
    id = np.argmax(sim_scores)
    return id+1


### Main Function ------------
def predict_anime_by_description(description:str, n:int=5, return_only_titles:bool=False):
    """
    predicts the anime name based on the description of anime genre.
    inputs description: string of anime description.
            n: length of output to return. if n=-1, return all
    return: if return_only_titles=false return dictionary of anime names, id and similarity score, length=n sorted by similarity score(reverted order).
            else return list of anime names length=n sorted by similarity score(reverted order).
    """
    predict_output = predict(vectorize_classes(tokenizer(description)), n, return_only_titles)

    return predict_output


def predict_anime_by_name(name:str, n:int=5, return_only_titles:bool=False):
    """
    predicts the anime name based on the classes using cosine similarity
    inputs name: string of anime name.
            n: length of output to return. if n=-1, return all
    return: if return_only_titles=false return dictionary of anime names, id and similarity score, length=n sorted by similarity score(reverted order).
            else return list of anime names length=n sorted by similarity score(reverted order).
    """
    id = get_anime_id_by_name(name)
    predict_output = predict(anime_classes.loc[id], n+1, return_only_titles)

    # prevent return the same of input anime.
    if not return_only_titles:
        for key, pred in predict_output.items():
            predict_output[key] = pred[1:]
    else:
        predict_output = predict_output[1:]

    return  predict_output


@inf_loops
@input_test
def main(*args, **kwargs):
    return predict_anime_by_name(*args, **kwargs)


if __name__ == "__main__":
    main(return_only_titles=True)

