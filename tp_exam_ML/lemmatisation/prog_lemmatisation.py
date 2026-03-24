# -*- coding: utf-8 -*-


import re

prefixes = [
    "mifampa","mifampi","mampa","mampi","maha","mam","manj","man","ma","mi","m",
    "nifampa","nifampi","nampa","nampi","naha","nanj","nam","nan","na","ni","n"
    "hifampa","hifampi","hampa","hampi","haha","hanj","ham","han","ha","hi","h"
    "fifampa","fifampi","fifan","fampi","fampa","faha","fam","fanj","fi","fan","fa",
    "mpam","mpanj","mpan","mpa","mpi",
    "voa",
  ]
suffixe = [
    "ina",
    "ana",
    "na"
  ]
prefixe_lettres = [
    "p", "b", "f", "v","t", "d", "s", "z","h","n"
  ]
suffixe_lettres = [
    "h","s","r","t","d","s","z","p","n"
  ]
mots_terminaison = [
    "ka","tra","na"
  ]
def load_dict(dict_path):
  mots_dict = set()
  try :
    with open(dict_path, "r", encoding="utf-8") as f:
      for line in f:
         mot = line.strip().lower()
         if mot:
          mots_dict.add(mot)
  except :
    print("Pas de dictionnaire")
  return mots_dict


def net_mot(mot):
    mot = mot.lower()
    mot = re.sub(r"[^\w\s]", "", mot)
    return mot

def pre_supp(mot):
  mots_option = []
  for prefix in prefixes:
    if mot.startswith(prefix):
      mot = mot[len(prefix):]
      mots_option.append(mot)
      for lettre in prefixe_lettres:
        mots_option.append(lettre+mot)
  if mots_option:
    return mots_option
  else:
    return [mot]


def suf_supp(mot):
  mots_option = []
  for suff in suffixe:
    if mot.endswith(suff):
      mot = mot[:-len(suff)]
      mots_option.append(mot)
      for lettre in suffixe_lettres:
        if mot.endswith(lettre):
          mots_option.append(mot[:-len(lettre)])
          for term in mots_terminaison:
            mots_option.append(mot[:-len(lettre)]+term)
      for term in mots_terminaison:
        mots_option.append(mot+term)
    else:
      mots_option.append(mot)

  return mots_option


def mot_exact(mots_option, mots_dict):
  for mot in mots_option:
    if mot in mots_dict:
      return mot
  return None

def lemmatisation(mot, mots_dict):
  mot = net_mot(mot)
  mots_option=[]

  mots_option1 = pre_supp(mot)

  for word in mots_option1:

    next_mot = suf_supp(word)
    for _ in next_mot:
      mots_option.append(_)
  mot_def = mot_exact(mots_option, mots_dict)
  if mot_def:
    return mot_def
  return("fototeny tsy ao anaty dictionnaire")

def prog_lemmatisation(mot):
  
  dict = load_dict("dict.txt")
  return lemmatisation(mot, dict)