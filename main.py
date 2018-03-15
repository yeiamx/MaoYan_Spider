from PCHelper import *
from MYSpider import *
import argparse



#print(spider.cinemaNameList)
#print(spider.cinemaDataList)

#print(spider.cinemaInfo)


"""parsing and configuration"""
def parse_args():
    desc = "Spider---maoyan cinema Info"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--offset', type=str, default='0',
                        help='offset', required=False)

    parser.add_argument('--limit', type=str, default='20',
                        help='limit num of infos you want', required=False)

    parser.add_argument('--results_path', type=str, default='results.txt',
                        help='The path of the txt file which stores the results', required=False)

    return parser.parse_args()
"""main"""
def main():
    # parse arguments
    args = parse_args()
    if args is None:
      exit()

    resultsFilePath = args.results_path
    resultsFile = open(resultsFilePath, 'w')

    maoyanUrl = "http://piaofang.maoyan.com/company/cinema"
    maoyanAPIUrlStarter = "http://piaofang.maoyan.com/cinema"
    spider = MYSpider(maoyanUrl)
    #spider.processData()
    spider.processDataWithRange(urlStarter=maoyanAPIUrlStarter, limit=args.limit, offset=args.offset)
    cinemaInfo = spider.cinemaInfo
    currentTime = spider.currentTime
    cinemaYearRecords = spider.cinemaYearRecords
    #print(currentTime)
    #print(cinemaInfo)
    #print(cinemaYearRecords)

    try:
        resultsFile.write("截至  "+currentTime)

        for key in cinemaInfo.keys():
            resultsFile.write('\n')
            resultsFile.write(key)
            resultsFile.write(" : ")
            resultsFile.write(str(cinemaInfo.get(key)))

            if (key!='全国'):
                resultsFile.write("\n票房年度信息：\n")
                yearList = cinemaYearRecords[key]['year']
                boxList = cinemaYearRecords[key]['box']
                for i in range(len(boxList)):
                    resultsFile.write(yearList[i]+" 票房为"+str(boxList[i])+"万\n")

            resultsFile.write('\n')
    finally:
        resultsFile.close()


if __name__ == '__main__':
    main()