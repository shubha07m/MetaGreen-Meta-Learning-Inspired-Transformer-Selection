import math
import numpy as np
import pandas as pd
from PIL import Image
from skimage.metrics import structural_similarity
from numpy import dot
from numpy.linalg import norm
from rembg import remove
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction


def img_similarity(fname1, fname2, sim_type, rmv_bg=0):
    # open images #

    f1 = Image.open(fname1)
    f2 = Image.open(fname2)

    # remove background #

    if rmv_bg == 1:
        f1 = remove(f1)
        f2 = remove(f2)

    # using .resize to scale image 2 to match image 1 dimensions #

    f1_reshape = f1.resize((round(f1.size[0]), round(f1.size[1])))
    f2_reshape = f2.resize((round(f1.size[0]), round(f1.size[1])))

    # convert the images to (R,G,B) arrays #

    f1_array = np.array(f1_reshape)
    f2_array = np.array(f2_reshape)

    # flatten the arrays to one dimensional vectors

    f1_array = f1_array.flatten()
    f2_array = f2_array.flatten()

    # divide the arrays by 255, the maximum RGB value to make sure every value is on a 0-1 scale #

    a = f1_array / 255
    b = f2_array / 255

    if sim_type == 1:
        cos_similarity = dot(a, b) / (norm(a) * norm(b))
        return cos_similarity
    if sim_type == 0:
        ssim = structural_similarity(a, b, data_range=1)
        return ssim


def txt_preprocess(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())

    # removing the stop words and non-alphanumeric words#
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    return Counter(tokens)  # tokenizing it


def txt_similarity(text1, text2):
    # preprocessing #

    vec1 = txt_preprocess(text1)
    vec2 = txt_preprocess(text2)

    intersection = set(vec1.keys()) & set(vec2.keys())  # calculating common words
    numerator = sum([vec1[x] * vec2[x] for x in intersection])  # calculating the dot products

    # calculating the magnitude of vectors

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])

    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    # Putting back to the cosine similarity formula

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def calculate_Lch(l, pb, t=2):
    pb_bar = pb
    Lch = 1

    for i in range(t + 1):
        binomial_coefficient = math.comb(l, i)
        Lch -= binomial_coefficient * (pb_bar ** i) * ((1 - pb_bar) ** (l - i))
    return Lch


def energy_penalty(df, img, model):
    model_df = df[(df['Image'] == img) & (df['Model Name'] == model)]
    if model_df.empty:
        return None

    max_power = df[df['Image'] == img]['Total Combined Power'].max()  # Vectorized operation
    power = model_df['Total Combined Power']
    normalized_power = power / max_power

    return normalized_power.iloc[0]


def comm_energy(semantics):
    p_max = 1
    max_data_rate = 143 * 10 ** 6

    message_length = countTotalBits(semantics)
    t = message_length / max_data_rate
    Ec = p_max * t

    message_length_max = 1500 * 8
    t_max = message_length_max / max_data_rate
    Ec_max = p_max * t_max

    return Ec / Ec_max


def countTotalBits(sem_string):
    bits = 8 * len(sem_string)
    return bits


def eosl_loss(df, img_name, encoder, Mi, Mp, pb=.001, lambda_es=1, lambda_sm=1, lambda_lch=1, lambda_ec=1):
    l_sem = countTotalBits(str(Mp))
    S_sm = txt_similarity(str(Mi), str(Mp))
    N_sm = 1 - S_sm
    L_ch = calculate_Lch(l_sem, pb)
    ec = comm_energy(Mp)
    es = energy_penalty(df, img_name, encoder)

    EOSL = lambda_sm * N_sm + lambda_lch * L_ch + lambda_ec * ec + lambda_es * es
    return EOSL, S_sm


def calculate_bleu_score(candidate, reference):
    """
    Calculate the Smoothed BLEU score of a candidate text compared to a reference text.

    Args:
    - candidate (str): The candidate text to be evaluated.
    - reference (str): The reference text.

    Returns:
    - bleu_score (float): The Smoothed BLEU score of the candidate text.
    """
    # Tokenize the candidate and reference texts
    candidate_tokens = nltk.word_tokenize(candidate)
    reference_tokens = nltk.word_tokenize(reference)

    # Create a smoothing function
    smoothie = SmoothingFunction().method3
    # keep it method3
    # Calculate the Smoothed BLEU score
    bleu_score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoothie)

    return bleu_score
