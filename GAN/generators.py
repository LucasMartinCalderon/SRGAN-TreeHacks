""" Defines the generator neural network for the GAN. """

import tensorflow as tf
from keras.models import Sequential, Model
from keras.layers import Lambda, UpSampling2D, Conv2D, Input, Concatenate
import keras.backend as K

from utils import to_float


def create_baseline_cnn(input_shape, output_size, resize_factor):
    """ Creates the generator for the GAN.

        Instantiates a Keras model which upsamples the input
        and performs a convolution, then resizes the image to fit output.

        Args:
            input_shape: A triple (x, y, channels) representing the input shape.
            output_size: A tuple (x, y) representing the output size.
            resize_factor: An integer factor by which to scale the input.

        Returns:
            model: The created Keras model.

    """

    model = Sequential()
    model.name = "generator"

    # Float Cast Layer
    model.add(Lambda(to_float, input_shape=input_shape))

    # Upsample Layer
    model.add(UpSampling2D(resize_factor))

    # Convolutional Layer
    model.add(Conv2D(filters=3, kernel_size=(3, 3), strides=(1, 1),
                     padding="SAME", activation="softplus"))

    # Resize Layer
    model.add(Lambda(lambda image: tf.image.resize_images(
        image, output_size,
        method=tf.image.ResizeMethod.BICUBIC,
        align_corners=True
        )))

    return model

def create_3colorsto1color_cnn(input_shape, output_size, resize_factor):
    def cnn_transform(inval, n_filters, kernel_size=(3, 3)):
        transformed = Conv2D(n_filters, kernel_size=kernel_size, padding="SAME", activation="softplus")(inval)
        summed = Lambda(lambda x: K.expand_dims( K.sum(x, axis=-1), ) ) (transformed)
        
        return summed

    img = Input(input_shape)

    # Float Cast Layer
    float_img = Lambda(to_float, input_shape=input_shape)(img)

    upsample = UpSampling2D(resize_factor)(float_img)

    GBR = []
    for i in range(3):  
        out = cnn_transform(upsample, n_filters=8)
        GBR.append(out)

    out_img = Concatenate()(GBR)
        
    # Resize Layer
    resized_img = Lambda(lambda image: tf.image.resize_images(
        image, output_size,
        method=tf.image.ResizeMethod.BICUBIC,
        align_corners=True
        ))(out_img)

    model = Model(inputs=[img], outputs=[resized_img])
    model.name = "generator"

    return model




def create_3colorsto1color_2layer_cnn(input_shape, output_size, resize_factor):
    def cnn_transform(inval, n_filters=8, kernel_size=(2,2)):
        transformed = Conv2D(n_filters, kernel_size=kernel_size, padding="SAME", activation='softplus')(inval)
        summed = Conv2D(1, kernel_size=(1,1), padding="SAME", activation="softplus")(transformed)
        return summed
    
    img = Input(input_shape)

    # Float Cast Layer
    float_img = Lambda(to_float, input_shape=input_shape)(img)
    upsample = UpSampling2D(resize_factor)(float_img)

    GBR = []
    for i in range(3):  
        out = cnn_transform(upsample, n_filters=8)
        GBR.append(out)

    out_img = Concatenate()(GBR)
        
    # Resize Layer
    resized_img = Lambda(lambda image: tf.image.resize_images(
        image, output_size,
        method=tf.image.ResizeMethod.BICUBIC,
        align_corners=True
        ))(out_img)

    model = Model(inputs=[img], outputs=[resized_img])
    model.name = "generator"

    return model


def create_3colorsto1color_2layer_MultiFilter_cnn(input_shape, output_size, resize_factor):
    
    
    def cnn_transform(inval, n_filters=4, kernel_sizes=[ (2,2), (3,3), (5,5), (7,7)]):
        outvals = []
        for size in kernel_sizes:
            out = Conv2D(n_filters, kernel_size=size, padding="SAME", activation='softplus')(inval)
            outvals.append(out)
            
        transformed = Concatenate()(outvals)
        summed = Conv2D(1, kernel_size=(1,1), padding="SAME", activation="softplus")(transformed)
        return summed
    
    img = Input(input_shape)
    float_img = Lambda(to_float, input_shape=input_shape)(img)
    upsample = UpSampling2D(resize_factor)(float_img)

    GBR = []
    for i in range(3):  
        out = cnn_transform(upsample, n_filters=8)
        GBR.append(out)

    out_img = Concatenate()(GBR)
    
    # Resize Layer
    resized_img = Lambda(lambda image: tf.image.resize_images(
        image, output_size,
        method=tf.image.ResizeMethod.BICUBIC,
        align_corners=True
        ))(out_img)

    model = Model(inputs=[img], outputs=[resized_img])
    model.name = "generator"

    return model


def create_2layer_baseline_cnn(input_shape, output_size, resize_factor):
    
    img = Input(input_shape)

    # Float Cast Layer
    float_img = Lambda(to_float, input_shape=input_shape)(img)
    upsample = UpSampling2D(resize_factor)(float_img)
    
    conv_out = Conv2D(32, kernel_size=(3, 3), activation='softplus')(upsample)
    out_img = Conv2D(3, kernel_size=(1,1), activation='softplus')(conv_out)
    
    # Resize Layer
    resized_img = Lambda(lambda image: tf.image.resize_images(
        image, output_size,
        method=tf.image.ResizeMethod.BICUBIC,
        align_corners=True
        ))(out_img)

    model = Model(inputs=[img], outputs=[resized_img])
    model.name = "generator"

    return model



def create_2layer_multiplFilters_cnn(input_shape, output_size, resize_factor):
    
    sizes = ( (2,2), (3,3), (5,5), (7,7) )
    n_filters = 4
    
    img = Input(input_shape)

    # Float Cast Layer
    float_img = Lambda(to_float, input_shape=input_shape)(img)
    upsample = UpSampling2D(resize_factor)(float_img)
    
    convs_out = []
    for size in sizes:
        conv_out = Conv2D(n_filters, kernel_size=size, activation='softplus', padding="SAME")(upsample)
        convs_out.append(conv_out)
        
    combined = Concatenate()(convs_out)
    out_img = Conv2D(3, kernel_size=(1,1), padding="SAME", activation='softplus')(combined)
    
    # Resize Layer
    resized_img = Lambda(lambda image: tf.image.resize_images(
        image, output_size,
        method=tf.image.ResizeMethod.BICUBIC,
        align_corners=True
        ))(out_img)

    model = Model(inputs=[img], outputs=[resized_img])
    model.name = "generator"

    return model





