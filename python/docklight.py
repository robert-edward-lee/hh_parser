








def getDataFromFile(name):
  with open("./docklight/%s.ptp"%name, "r+", encoding = "utf-8") as file:
    data = file.read()
  return data


def saveDataToFile(data):
  return


def updateData(data):

  return


data = getDataFromFile("MLINK_SIM")

print(data)


