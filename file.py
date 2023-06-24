def save_to_file(file_name, jobs):
    #file Open
    file = open(f"{file_name}.csv", "w")
    #문서의 title
    file.write("Position,Company,Location,URL\n")
    #jobs의 Data를 CSV 형식으로 Write
    for job in jobs:
        file.write(f"{job['position']},{job['company']}, {job['location']}, {job['link']}\n")

    file.close()