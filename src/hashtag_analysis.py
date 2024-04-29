


tmp = []
tmp.append(("name1", 0.34627))
tmp.append(("name2", 0.34627))
tmp.append(("name3", 0.34627))
tmp.append(("name4", 0.34627))
tmp.append(("name5", 0.34627))



def extract_hashtags(quartile, hashtags):

    quartile_hashtags = []

    for qrow in quartile:
        for hrow in hashtags:
            if(qrow[0] == hrow[0]):
                quartile_hashtags.extend(hrow[1])


    # Save file







def main():
    extract_hashtags(range_0_25)
    print("Extracted hashtags for the first quartile")

    extract_hashtags(range_26_50)
    print("Extracted hashtags for the second quartile")

    extract_hashtags(range_51_75)
    print("Extracted hashtags for the third quartile")

    extract_hashtags(range_76_100)
    print("Extracted hashtags for the fourth quartile")