import os
import stat
from support import ElementTree

def get_folders(xml_response, folder_path):
    """Add information about the folders in [folder_path] to
    [xml_response].
    """

    folders = ElementTree.Element("Folders")

    for f in os.listdir(folder_path):
        if os.path.isdir(f):
            folders.append(ElementTree.Element("Folder",
                                               {'name' : f}))

    xml_response.getroot().append(folders)

def get_folders_and_files(xml_response, folder_path):

    folders = ElementTree.Element("Folders")
    files = ElementTree.Element("Files")

    for f in os.listdir(unicode(folder_path)):
        if os.path.isdir(os.path.join(folder_path, f)):
            folders.append(ElementTree.Element("Folder",
                                               {'name' : f}))
        else:
            size = os.lstat(os.path.join(folder_path, f))[stat.ST_SIZE]
            size = str(size / 1024)

            files.append(ElementTree.Element("File",
                                             {'name' : f,
                                              'size': size}
                                             )
                         )

    xml_response.getroot().append(folders)
    xml_response.getroot().append(files)


def file_upload(request, folder_path):
    """Handle a file upload and return the status code."""

    new_file = request.FILES.get('NewFile', None)
    if new_file is None:
        status = "202"
    else:
        # determine the destination file name

        #0.96
        #file_name = new_file['filename']
        #1.0
        file_name = new_file.name.decode('utf-8')
        file_content = new_file.read()

        base, ext = os.path.splitext(new_file.name)
        count = 1

        while (os.path.exists(os.path.join(folder_path, file_name))):
            file_name = '%s(%s)%s' % (base, count, ext)
            count += 1

        # write the file
        target = file(os.path.join(folder_path, file_name), 'wb')

        target.write(file_content)
        target.close()

        # set the status
        if file_name == file_name:
            status = "0"
        else:
            status = "201"

        return status, file_name


##     new_file = request.FILES.get('NewFile', None)

##     if new_file is None:
##         status = "202"
##     else:
##         # determine the destination file name
##         file_name = new_file['filename']
##         base, ext = os.path.splitext(new_file['filename'])
##         count = 1

##         # XXX need to determine resource_type here
##         resource_type = 'Image' #request.REQUEST.get('Type', None)

##         while (os.path.exists(actual_path(settings.FCKEDITOR_CONNECTOR_ROOT,
##                                           resource_type, file_name))):
##             file_name = '%s(%s)%s' % (base, count, ext)
##             count += 1

##         abs_path =  actual_path(settings.FCKEDITOR_CONNECTOR_ROOT,
##                                 resource_type, file_name)
##         abs_url  =  actual_url(settings.FCKEDITOR_CONNECTOR_URL,
##                                 resource_type, file_name)

##         # write the file
##         target = file(os.path.join(abs_path, file_name), 'wb')
##         target.write(new_file['content'])
##         target.close()

##         # set the status
##         if file_name == new_file['filename']:
##             status = "0"
##         else:
##             status = "201, '%s'" % file_name
