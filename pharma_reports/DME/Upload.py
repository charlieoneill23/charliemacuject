from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import warnings

warnings.filterwarnings('ignore')
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)


class Upload:
    """
    A class used to upload the required dataframes to Google Drive.

    ...

    Attributes
    ----------
    folder : str
        a formatted string to determine the folder to upload to
        options: 'pharma_reports', 'research'
    dr_name : str
        a formatted string of audited doctor, used to create folder in drive
    file_list : list
        a list of files to upload to Drive

    Methods
    -------
    set_folder(self)
        Determines the path ID of the folder to upload to.
    view_files(self)
        View all folders and file in the Google Drive.
    create_folder(self)
        Create folder on Google Drive.
    upload_files(self)
        Upload the specified file of the object.
    """

    def __init__(self, folder, dr_name, file_list):
        self.folder = folder
        self.dr_name = dr_name
        self.file_list = file_list

    def retrieve_files(self):
        """
        Returns a list of files in the main directory to upload.
        """
        if self.file_list == 'all':
            return ['initialmetrics.csv', 'drug_int_metrics.csv', 'interval_metrics.csv',
                    'interval_distribution.csv', 'int_dist_plot.csv',
                    'visual_metrics.csv', 'drug_dist_table.csv', 'va_distributions.csv',
                    'ut_plot.png', 'anchor.csv']

    def set_folder(self):
        """
        Determines the path ID of the folder to upload to.
        Input: self.
        Output: folder_id (PyDrive object)
        """
        if self.folder == 'pharma_reports':
            folder_id = '1tzvQ-xBZOy6_zA5EPbnQ5nEDENurAj1N'
        elif self.folder == 'research':
            folder_id = '1GuUeRc7Zqe5GdM1dmJOUF6VPW5NklH-R'
        else:
            folder_id = '1INvWwtJhtiD4vqCEpehd4RT06I1-50pU'
        return folder_id

    def view_files(self):
        """
        View all folders and file in the Google Drive.
        """
        fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file in fileList:
            print('Title: %s, ID: %s' % (file['title'], file['id']))

    def create_folder(self):
        """
        Create folder on Google Drive.
        """
        folder_name, parent_folder_id = self.dr_name, self.set_folder()
        folder_metadata = {'title': folder_name,
                           # Define the file type as folder
                           'mimeType': 'application/vnd.google-apps.folder',
                           # this is ID of the parent folder
                           'parents': [{"kind": "drive#fileLink", "id": parent_folder_id}]}
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        # Return folder informations
        return folder['id']

    def upload_files(self):
        """
        Upload the specified file of the object.
        """
        folder_id = self.create_folder()
        upload_file_list = self.retrieve_files()
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
            # Read file and set it as the content of this instance.
            gfile.SetContentFile(upload_file)
            gfile.Upload()  # upload the file.
