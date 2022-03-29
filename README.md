# Nice Shot!

**Nice Shot!** is an open-source project which focuses on analysing specific player movements with the help of computer vision. Its main objective is to help those learning tennis to practice performing certain shots, such as forehand and backhand. The recognition system is aimed at people of all ages and levels of expertise, so whether you'd like to help your child practice or you're aiming at getting back into shape, **Nice Shot!** is for you!  

This project is a collaboration between Team 1 of UCL's 2021/22 COMP0016 module consisting of Morgane Ohlig, Jin Feng and Prithvi Kohli and [InfoSys](https://www.infosys.com) as part of UCL's [Industry Exchange Network](https://www.ucl.ac.uk/computer-science/collaborate/ucl-industry-exchange-network-ucl-ixn).  

This system currently supports the following shots; forehand, backhand, smash, service.

## Features
- Extraction of poses from videos with [MediaPipe](https://mediapipe.dev);
- Recognition and classification of tennis shots with [Tensorflow](https://www.tensorflow.org) using the Convolutional Neural Network Model and the Spatial-Temporal Graph Convolutional Network;
- Reconstruction of poses with 3D skeletons in [Three.js](https://threejs.org).

## Dependencies
- [Numpy](https://numpy.org/)
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev)
- [Tensorflow](https://www.tensorflow.org)
- [SciPy](https://scipy.org/)
- [Flask](https://flask.palletsprojects.com/en/2.1.x/)

## Deployment
1. Ensure the above dependencies are installed and that you are running Python 3.8.
2. cd into 'src' and run 'python app.py' to start the Flask server.
3. The webapp can then be accessed by navigating to ‘localhost:5000’.
4. Analysis results are stored in the folder 'src/static/analysis_results'
5. If you wish to use the analysis pipeline API, please refer to the provided documentation on the project website.

## Links and Additional Resources
- [Development blog](https://ucl-comp16-2021-team1.github.io/blog/)
