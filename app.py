# doing necessary imports
import threading
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import logging
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin
import pandas as pd
from mongoDBOperations import MongoDBManagement
from FlipkratScrapping import FlipkratScrapper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



logging_str = "[%(asctime)s: %(levelname)s: %(module)s] %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename= os.path.join(log_dir,"Scrapper.log"),level=logging.INFO, format=logging_str, filemode="a")


app = Flask(__name__)  # initialising the flask app with the name 'app'

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

# base url + /
#http://localhost:8000 + /
@app.route('/result',methods=['POST']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
        try:
            ebayUrl = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=" + searchString # preparing the URL to search the product on flipkart
            uClient = uReq(ebayUrl) # requesting the webpage from the internet
            EbayPage = uClient.read()# reading the webpage
            uClient.close()# closing the connection to the web server
            EBAY_html = bs(EbayPage, "html.parser") # parsing the webpage as HTML
            bigboxes = EBAY_html.findAll("div", {"class": "s-item__wrapper clearfix"}) # seacrhing for appropriate tag to redirect to the product link
            box = bigboxes[2] #  taking the first iteration (for demo)
            productLink =  box.div.div.a['href']
            prodRes  = requests.get(productLink)
            prod_html = bs(prodRes.text, "html.parser") # parsing the product page as HTML
            commentboxes = prod_html.findAll('div', {'class':'ebay-review-section'}) # finding the HTML section containing the customer comments

            reviews = [] # initializing an empty list for reviews
            #  iterating over the comment section to get the details of customer and their comments
            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.span.find_all('div', {'class': 'a-profile-content'})[0]

                except:
                    name = 'No Name'

                try:
                     rating_count=0
                     a=[]
                     for stars in commentbox.div.div.span:
                         if stars!='\n':
                             rating_count=rating_count+1
                     rating=rating_count

                except:
                    rating = 'No Rating'

                try:
                    commentHead = commentbox.find_all('div',{'class':'ebay-review-section-r'})[0].p.text
                except:
                    commentHead = 'No Comment Heading'

                try:
                    comtag = commentbox.findAll('div',{'class':'ebay-review-section-r'})
                    souptag=bs(str(comtag[0]),'html.parser')
                    custComment=souptag.select_one('.ebay-review-section-r p:nth-of-type(2)').text

                except:
                    custComment = 'No Customer Comment'

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
            return render_template('results.html', reviews=reviews) # showing the review to the user
        except:
            return 'something is wrong in the process'


if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000