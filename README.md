# Identity-Authentication-Using-Face-Verification-and-ID-Image-Recognition-
We designed a service that uses face verification and ID card recognition to perform personal identity authentication automatically. First, the user supposed to create an account by choosing an email and password and entering contact information. After creating an account, user logs in the application with his/her email and password. If the user logs in successfully, the user supposed to upload a photo of the ID card. The program extracts and verifies data in real time automatically from the ID card. Then the program will take video and extracts a few photos from the video to catch the users face correctly. System will compare the photo on the ID card with the photo taken from camera and gives a result. If all the stages are passed, the identity authentication will be validated in seconds automatically.

<img width="282" alt="Picture1" src="https://user-images.githubusercontent.com/44849765/199513318-f140be71-01a7-4acd-8761-163c9233de25.png">

<img width="311" alt="Picture2" src="https://user-images.githubusercontent.com/44849765/199513345-e5843808-641a-4761-af3f-5fe8873598ec.png">


<img width="503" alt="Ekran Resmi 2021-08-17 19 07 17" src="https://user-images.githubusercontent.com/44849765/129762155-cd509d7c-a3a5-46a3-96bc-20c2c04ed0b0.png">

Processing of information extraction from ID card:

<img width="545" alt="Ekran Resmi 2021-08-17 19 16 21" src="https://user-images.githubusercontent.com/44849765/129762835-f1efc031-b0b2-43fb-b548-669514184390.png">

Example of non-match:

<img width="402" alt="Ekran Resmi 2021-08-17 19 12 19" src="https://user-images.githubusercontent.com/44849765/129762589-44178929-b08c-4302-9f17-4cc9f32d90df.png">

Example of match:

<img width="402" alt="Ekran Resmi 2021-08-17 19 12 38" src="https://user-images.githubusercontent.com/44849765/129762481-4f9b2c74-612c-4de3-8731-3888bd3cfd97.png">


In this project, during the development of the face verification system, training was conducted on pre-trained models using the CASIA-WebFace dataset.
In this study, different experiments were carried out in order to compare the performance of the models.
In the first model a; flatten and dense layers were added on the pre-trained vgg16 (with resnet-50 architecture) model. We did the last layer trainable and there were 5,346,841 trainable values in the model after adding the layers. For this model, we split the CASIA-WebFace dataset and took 25 classes of it to train and test the model. We split it like 80 train, 10 validation, 10 test data. The accuracy was 0.70 after training 10 epoch.
In the second model b; flatten and dense layers were added on the pre-trained vgg16 (with resnet-50 architecture) model just like the a model. We did the last four layers trainable and there were 7,288,516 trainable values in the model. We use the 25 classes of the dataset like first model to train and test. We split it like 80 train, 10 validation, 10 test data. The accuracy was 0.73 after training 10 epoch.
In the third model c; flatten layer, 2 dense(512) layer, 1 dense(256) layer were added on the pre-trained VGGFace model. There were 13,239,552 trainable values in the model after adding the layers. For this model, we split the CASIA-WebFace dataset and took 100 classes of it to train and test the model. We split it like 80 train, 10 validation, 10 test data. The accuracy was 0.82 after training 20 epochs.
In the last model d; flatten layer, 2 dense(512) layer, 1 dense(256) layer were added on the pre-trained VGGFace model just like the c model.But this time we trained the model on 256 classes taken from CASIA-WebFace. We split it like 80 train, 10 validation, 10 test data. The accuracy was 0.83 after training 20 epochs.

If we look at the models that we have trained, we can say that the most successful model is the last one (d model). When we compare the first two models, we can say that if there is more trainable values, the accuracy increase because the other conditions are the same for the model a and b. When we look at the c and d models, d model gives slightly better results because that the class number is more than the c model.

The comparisons of the models is below.

<img width="515" alt="Ekran Resmi 2021-08-17 19 20 34" src="https://user-images.githubusercontent.com/44849765/129763395-b5c87bc5-6d16-4605-a755-47498675700a.png">
