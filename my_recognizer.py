import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    
    for idx, _ in test_set.get_all_Xlengths().items():
        X, lengths = test_set.get_item_Xlengths(idx)
        
        LogL_dict = {}
        for word, model in models.items():
            try:
                LogL_dict[word] = model.score(X, lengths)
                
            except:
                LogL_dict[word] = float("-inf")
        
        probabilities.append(LogL_dict)
        
        guesses.append(max(LogL_dict, key=LogL_dict.get))
        
    return probabilities, guesses
