from wordcloud import WordCloud 
import consts
import os

def madeCloudOfWords():
    d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    text = open(os.path.join(d, consts.ARQ_TXTFORCLOUD)).read()

    # Generate a word cloud image
    wordcloud = WordCloud(width=1600, height=800, background_color="white", repeat=False, collocations=False)
    wordcloud.generate(text)
    wordcloud.to_file("keywordsFromVocabulary.png")

if __name__ == "__main__":
    madeCloudOfWords()