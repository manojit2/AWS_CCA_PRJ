import glob
import sys
import os
import re


def prep_samplefiles():
    path = '*.txt'
    files = glob.glob(path)
    data_list = []
    article_list = []
    os.remove("comments.txt")

    with open('comments.txt', 'a') as fo:
        for file in files:
            comments = []
            article_data = {}
            line_num = 0
            title = ''
            source = ''
            date_pub = ''
            url_pub = ''
            doc_id = ''.join(re.findall(r'\d+', file))
            comments_out = ''
            with open(file, 'r') as fp:
                for cnt, line in enumerate(fp):
                    if cnt == 0:
                        title = line.strip('\n')
                    elif cnt == 1:
                        # print("URL: {}".format(line))
                        url_pub = line.strip('\n')
                    elif cnt == 2:
                        # print("Date: {}".format(line))
                        date_pub = line.strip('\n')
                    elif cnt == 3:
                        # print("Source: {}".format(line))
                        source = line.strip('\n')
                    elif cnt >= 4:
                        if ('avatar') in line.lower():
                            pass
                        else:
                            comments.append(line.lower().strip('\n'))
                # print("## {} \n".format(doc_id))

                comments_out = ''.join(comments)
                # print(comments_out)
                # print("")
                # print("")
            # fo.writelines('## '+doc_id + '\n')
            # fo.writelines(comments_out + '\n')
            data_out = '## ' + doc_id + ', ' + title + ', ' + source + ', ' + date_pub + ', ' + url_pub
            # data_article = {'doc_id': doc_id, 'title':title, 'source':source, 'date_pub':date_pub, 'url': url_pub}
            article_list.append(data_out)
        fo.close()
        os.remove('articles.txt')
        with open('articles.txt', 'a', encoding='UTF-8') as fo:
            for article in article_list:
                fo.writelines(str(article) + '\n')

        return article_list
