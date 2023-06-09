from system import System
from typing import Callable
from firebase_admin import credentials, initialize_app, storage, firestore
from google.api_core.exceptions import NotFound
from google.cloud.firestore_v1.watch import Watch
import firebase_admin
import os
import time
    

class Firebase():

    def __init__(self):
        
        if not firebase_admin._apps:

            credential = credentials.Certificate(os.environ.get('FIREBASE_KEY_PATH'))
            initialize_app(credential) 
        
        self.firestore = firestore.client()


class FirebaseLogIn(Firebase):

    def __init__(self) -> None:

        super().__init__()


    def validade_device(self, user: str, device: str) -> bool:

        ref = self.firestore.collection(user).document(device)        

        return ref.get().exists


class FirebaseSignUp(Firebase):

    def __init__(self):
        
        super().__init__()
        

    def queue_device(self, device: str):
        
        self.__device = device
        self.firestore.collection('QueuedRaspberrys').document(self.__device).set({'user': 'None'})


    def wait_for_user(self) -> str:

        watch = self.firestore.collection('QueuedRaspberrys').document(self.__device)\
            .on_snapshot(self.__on_snapshot_callback)

        self.__user = 'None'

        while self.__user == 'None':
            time.sleep(0.5)

        watch.unsubscribe()

        return self.__user


    def __on_snapshot_callback(self, snapshot, changes, read_time) -> None:

        for change in changes:

            if change.type.name != 'MODIFIED':
                break

            incoming = change.document.to_dict()
            self.__user = incoming['user']


    def add_device(self) -> None:

        printer_defaults = {
            'name'     : 'undefined',
            'hotend'   : {'setpoint': 0, 'current': 25},
            'heatbed'  : {'setpoint': 0, 'current': 25},
            'status'   : 'booting',
            'command'  : 'G0',
            'updated'  : 'None',
            'streaming': False,
            'baudrate' : 250000
        }

        self.firestore.collection(self.__user).document(self.__device).set(printer_defaults)

        self.firestore.collection('QueuedRaspberrys').document(self.__device).delete()


class Database(Firebase):

    def __init__(self, user: str, device: str):

        super().__init__()
        
        # System paths
        self.firebase_storage_path = 'print_file.gcode'
        self.print_file_path = System.local_print_file_path
        
        # Set up database
        self.__database = self.firestore.collection(user).document(device)
        self.update_status('idle')

        # Set up storage
        bucket = storage.bucket(os.environ.get('FIREBASE_BUCKET_PATH'))
        self.__storage = bucket.blob(self.firebase_storage_path)

    
    def set_up_database_watch(self, callback: Callable) -> Watch:
        """Receives the function that will be called when the database is updated"""

        firebase_watch = self.__database.on_snapshot(callback)

        return firebase_watch


    def read(self, id: str):
        return self.__database.get().to_dict().get(id)


    def update_database(self, collection: dict = {}) -> None:
        
        param = collection.copy()

        param['updated'] = 'None'
        
        try:
            self.__database.update(param)

        except NotFound:
            pass

        del param


    def update_status(self, _status: str) -> str:
        
        self.update_database({'status': _status})
        
        return _status
    

    def download_file(self) -> None:
        self.__storage.download_to_filename(System.local_print_file_path)


    def wait_user_request_to_boot(self) -> bool:
        """Awaits for user>device>status to be equal to 'boot'"""

        self.__should_boot: bool = False
        self.__user_available: bool = True

        watch = self.set_up_database_watch(self.__boot_callback)

        while not self.__should_boot and self.__user_available:
            time.sleep(0.1)
        
        watch.unsubscribe()

        return self.__user_available
    

    def __boot_callback(self, snapshot, changes, read_time) -> None:

        for change in changes:
            
            # In case a attribute has changed
            if change.type.name == 'MODIFIED':
                incoming = change.document.to_dict()
                self.__should_boot = (incoming['status'] == 'boot')

            # In case the user was deleted
            elif change.type.name == 'REMOVED':
                self.__user_available = False
                

