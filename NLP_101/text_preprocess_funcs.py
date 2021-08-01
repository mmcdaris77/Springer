import re, string, unicodedata
import nltk
import contractions
import inflect
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from bs4 import BeautifulSoup
print("versions \n ------------------------------")
print("nltk: {}".format(nltk.__version__))
print("inflect: {}".format(inflect.__version__))
# print("contractions: {}".format(contractions.__version__))

# https://www.kdnuggets.com/2018/03/text-data-preprocessing-walkthrough-python.html
# https://www.kdnuggets.com/2017/12/general-approach-preprocessing-text-data.html
'''
STUFF TO ADD
- remove email address
- remove URL
'''

# START DENOISE STEPS
def strip_html(text): 
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()


def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)


def denoise_text(text):
    #text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text

# START TOKENIZATION STEPS
def replace_contractions(text):
    return contractions.fix(text)


def get_tokeinzed_words(text):
    return nltk.word_tokenize(text)

# START NORMALIZATION STEPS
def remove_non_ascii(words):
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def to_lower(words):
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words


def remove_punctuation(words):
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def replace_numbers_w_word(words):
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words


def remove_stopwords(words):
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words


def stem_words(words):
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems


def lemmatize_words(words):
    lemmatizer = WordNetLemmatizer()
    lems = []
    for word in words:
        lem = lemmatizer.lemmatize(word, pos='v')
        lems.append(lem)
    return lems


def normalize(words):
    words = remove_non_ascii(words)
    words = to_lower(words)
    words = remove_punctuation(words)
    words = replace_numbers_w_word(words)
    words = remove_stopwords(words)
    return words


def stem_and_lemmatize(words):
    stems = stem_words(words)
    lems = lemmatize_words(words)
    return stems, lems

if __name__ == '__main__':
    print("START")
  
    from sklearn import feature_extraction
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer

    sample = """<h1>Title Goes Here</h1>
                <b>Bolded Text</b>
                <i>Italicized Text</i>
                <img src="this should all be gone"/>
                <a href="this will be gone, too">But this will still be here!</a>
                I run. He ran. She is running. Will they stop running?
                I talked. She was talking. They talked to them about running. Who ran to the talking runner?
                [Some text we don't want to keep is in here]
                ¡Sebastián, Nicolás, Alejandro and Jéronimo are going to the store tomorrow morning!
                something... is! wrong() with.,; this :: sentence.
                I can't do this anymore. I didn't know them. Why couldn't you have dinner at the restaurant?
                My favorite movie franchises, in order: Indiana Jones; Marvel Cinematic Universe; Star Wars; Back to the Future; Harry Potter.
                Don't do it.... Just don't. Billy! I know what you're doing. This is a great little house you've got here.
                [This is some other unwanted text]
                John: "Well, well, well."
                James: "There, there. There, there."
                &nbsp;&nbsp;
                There are a lot of reasons not to do this. There are 101 reasons not to do it. 1000000 reasons, actually.
                I have to go get 2 tutus from 2 different stores, too.
                22    45   1067   445
                {{Here is some stuff inside of double curly braces.}}
                {Here is more stuff in single curly braces.}
                [DELETE]
                </body>
                </html>"""
    
    sample = denoise_text(sample)
    #print(sample)
    sample = replace_contractions(sample)
    #print(sample)
    words = get_tokeinzed_words(sample)
    #print(words)
    words = normalize(words)
    #print(words)
    stems, lems = stem_and_lemmatize(words)
    #print(words)
    #print('Stemmed: \n{}\n'.format(stems))
    #print('Lemmatized: {}'.format(lems))
    #print(type(words))

    vocab_frame = pd.DataFrame({'words': words}, index=stems)
    print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')
    print(vocab_frame)
    '''
    tfidf_vectorizer = TfidfVectorizer(max_df=0.5, max_features=200000,
                                        min_df=0.2, stop_words='english',
                                        use_idf=True, tokenizer=get_tokeinzed_words,
                                        ngram_range=(1, 5))

    tfidf_matrix = tfidf_vectorizer.fit_transform(sample) # fit the vectorizer to synopses

    print(tfidf_matrix.shape)
    '''
    print("DONE")