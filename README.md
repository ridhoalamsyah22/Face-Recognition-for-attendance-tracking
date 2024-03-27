Face Recognition for attendance tracking:

1. init.py

This file is run the first time you run the program.
The function of this file is to create a dataset folder and a trainer folder. where the trainer folder contains "trainer.yml".
besides that this file also downloads "haarcascade_frontalface_default.xml" which will be used as a model for face recognition.

3. take_sample.py

This file serves to take an image to be used as a dataset.
   
4. train_image

This file serves to train the model so that it can recognize faces whose data comes from the dataset.
 
5. absensi

This file is the final file used to recognize faces and send the data results to excel (absensi.xslx).


**NOTE** :

You can delete the files in the dataset folder and fill it with new datasets.

Here is how to fill an empty dataset file:
1. running program take_sample.py
2. wait until program cathct your picture with your cameras.
3. done
