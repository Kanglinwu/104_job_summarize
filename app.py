from flask import Flask, render_template, jsonify
from bs4 import BeautifulSoup

import requests



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/<target>')
def index(target):
    # area = 6001006000 Hsinchu
    templist = []
    target_url = f'https://www.104.com.tw/jobs/search/?keyword={target}&area=6001006000&jobsource=2018indexpoc&ro=0'
    # # using header as smart phone
    # headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    # start request
    origin_result = requests.get(target_url)

    ## Using the bs4 to findall hyperlink
    soup = BeautifulSoup(origin_result.content,'html.parser')
    ## Search all a href
    list_tags = soup.find_all('a')

    ## for it
    for hyperlink in list_tags:
        ## check the link with job
        if 'www.104.com.tw/job/' in hyperlink.get('href'):
            ## append to list by dict type
            templist.append(dict(company=hyperlink.text, hyperlink=hyperlink.get('href')))
            # print(hyperlink.text, ' -- ', hyperlink.get('href'))
        # print(hyperlink)
    
    print(templist)


    # print(origin_result.status_code)
    # print(origin_result.content)

    # Save the result to file to see
    fp = open('templates/result_104.html', 'a', encoding='utf-8')
    fp.truncate(0)
    fp.write(origin_result.text)
    fp.close()
    return render_template('result_104.html')

    # return jsonify(templist)


if __name__ == '__main__':
    app.run(debug=True, port=9240)