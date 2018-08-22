import os
import codecs


def getItemsInDir(directory: str, flags: int = 0, sort=False, reverse=False) -> list:
    """
    :param directory: 将要列出文件的目录
    :param flags: 标记, 0 - 列出全部, 1 - 文件, 2 - 目录
    :return: 根据标记返回对应的items
    """
    try:
        allfiles = os.listdir(directory)
        if sort:
            allfiles.sort(reverse=reverse)

        dirs = []
        files = []
        for item in allfiles:
            tItemPath = directory + '/' + item
            if os.path.isfile(tItemPath):
                files.append(tItemPath)
            elif not item.startswith('.'):
                dirs.append(tItemPath)
             
        if flags == 0:
            dirs.extend(files)
            return dirs
        elif flags == 1:
            return files
        else:
            return dirs
    except Exception as e:
        print(str(e))
        return []

if __name__ == '__main__':
    genContent = ""
    genContent += "# Catalog\n\n"
    curPath = os.getcwd()
    dirs = getItemsInDir(curPath, flags=2, sort=True, reverse=True)
    dirs = list(filter(lambda x: not x.startswith('.'), dirs))
    print("dirs sorted:", dirs)

    for tDir in dirs:
        items = getItemsInDir(tDir, sort=True, reverse=True)
        
        filteredItem = list(filter(lambda x: (x.split('.')[-1]=="md"), items))
        filteredItemName = [x.split('/')[-1] for x in filteredItem]
        print("filteredItem:", filteredItemName)
        dirSplited = tDir.split('/')
        genContent += "\n## %s\n\n"%(dirSplited[-1])
        for item in filteredItem:
            itemName = item.split('/')[-1]
            linkAddress = "./%s/%s)\n</br>"%(dirSplited[-1], itemName)
            linkAddress = linkAddress.replace(' ', '%20')
            genContent += "[%s](%s)"%(itemName.split('.md')[-2], linkAddress)

    genContent += "\n\n"
    print(genContent)
    
    with codecs.open(curPath+"/README.md", 'w', 'utf-8-sig') as f:
        f.write(genContent)

