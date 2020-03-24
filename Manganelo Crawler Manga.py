import os
import cfscrape
from bs4 import BeautifulSoup


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def main():
    print ("######################################################")
    print ("Can full chapter or specific chapter")
    print ("Automatic create manga name folder")
    print ("Example: https://manganelo.com/manga/domestic_na_kanojo")
    print ("Leave blank for exit")
    print ("######################################################")

    while True:
        print("-------------------")
        url = input('Enter manga url: ')
        url.replace(" ", "")
        if len(url) < 1:
            break

        scrape = cfscrape.create_scraper()
        html = scrape.get(url).content
        soup = BeautifulSoup(html,features="lxml")
        chapter_list = []
        link_list = []

        for ultag in soup.find_all('ul', {'class': 'row-content-chapter'}):
            for litag in ultag.find_all('a'):
                chapter_list.append(litag.text)
                link_list.append(litag['href'])
        chapter_list.reverse()
        link_list.reverse()
        series_name = soup.find('div', {'class': 'story-info-right'}).find("h1").getText()
        print("\n",series_name,"\n")
        for number, chapter in enumerate(chapter_list):
            print(str(number+1) + ".", chapter)
        print("")
        chapter = input('Chapter Chosen(example 1-100, left number): ')
        try:
            dari_chapter, akhir_chapter = chapter.split("-")
            chapter_list = chapter_list[int(dari_chapter)-1:int(akhir_chapter)]
            link_list = link_list[int(dari_chapter)-1:int(akhir_chapter)]
        except:
            dari_chapter = chapter
            chapter_list = chapter_list[int(dari_chapter)-1]
            link_list = [link_list[int(dari_chapter)-1]]
        folder = input('Folder to Save (example D:/Manga): ')
        folder = folder + "\\"
        for chap in link_list:
            print("\n",chap,"\n")
            if (folder == "exit\\"):
                break
            http, empty, page, string, serie, chapter = chap.split("/")
            newhtml = scrape.get(chap).content
            newsoup = BeautifulSoup(newhtml,features="lxml")
            image_list = [tag.findAll('img') for tag in newsoup.findAll('div', {"class": "container-chapter-reader"})]

            def download_image(image_response, image_number):
                path_directory = folder + series_name + "\\" + chapter
                path_directory = path_directory.replace('\\\\', '\\')
                file_name = "{}.png".format("img-" + "%03d" % (image_number,))
                if image_response.status_code == 200:
                    if not os.path.exists(path_directory):
                        os.makedirs(path_directory)
                    with open(path_directory + "\\" + file_name, 'wb') as out_file:
                        for data in image_response:
                            out_file.write(data)
                        print (path_directory)
                        print (file_name)
                else:
                    print (image_response.status_code)

            counter = 0
            for img in image_list[0]:
                download_image(scrape.get(img['src']), counter)
                counter += 1


if __name__ == "__main__":
    main()
