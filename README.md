#Product Spec is Design Tool product's data#


*Please follow the steps to update the new product data*

##Preparation##

Download any git tool and clone this project to your pc

git tool: [TortoiseGit](https://tortoisegit.org/)

[Step by step](https://docs.google.com/presentation/d/13R_uY1wWkM9xs4NZTqyKzN9lQGDJ54UFV-vRLM-i3F0/edit#slide=id.g10864fa8cc_1_1)

[Install Anaconda](https://docs.anaconda.com/anaconda/install/)

Execute Anaconda Prompt

##Products##

1. Choose/Create a branch you want to add (ex: **nuuo**)

2. Choose/Create a product (ex: **Mainconsole CT-8000IP**)
**note**: Please create a **product_name.json** in this product
folder if this is a new product. You can copy and paste from other
product and replace the detail

3. Choose/Create a camera type (ex: **IP Camera**) or a CPU model (ex: **Intel Core i7-4770S @ 3.10GHz**)

4. Choose/Create a video format (ex: **H.264**)

5. Put your data in this folder with naming **1.csv**, **2.csv**, and so on. Please make sure that your data sheet does not contain any format (you can use **data_template.csv** in the home folder)

6. Create a **config.json** in this folder. This file specifies where to find the coef. For example, **"ivs\_rf": 1** means the you want to take coef ivs_rf from 1.csv

7. Go back to home folder and execute **generate.py**, check the result in product_specs.js

**P.S. You can copy x.csv from other product and replace the data to avoid format issue while running generate.py**

###Data sheet format###

All the headers must be **100% the same** as the following, **new line is not acceptable**. Header name are

- Local Decode(TotalCH*Resolution*FPS)

- Local Decode(Total Bit Rate)

- Smart Guard(General Motion)(Total DecodeResolution*FPS)

- Smart Guard(General Motion)(Total Decode Bit Rate)

- Smart Guard(General Motion)(Total DecodeResolution*FPS)(Pure)

- Live View Connection(Server Total UpLoad Bit Rate)

- Always Record(Total Record Bit Rate)

- Metadata

- Edge Event

- IVS Channel(Resolution*FPS)

- IVS Channel(Bit Rate)

- IVS Channel(Resolution*FPS)(Pure)

- const **Required column**

- Loading Avg **Required column**


##Client PC##

The same as products

##Cameras##

Does not support yet