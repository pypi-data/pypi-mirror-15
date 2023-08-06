.. Image2PyArray
   =========================

Image2PyArray: TensorFlow画像読み込み
=====================================

+ 組み合わせが必要な場合(一つの画像を入力として複数の教師信号が1になる場合)は使えません
+ zipなどを展開せず読めます

使い方
-----------

.. code-block:: pycon

    >>> from image2pyarray import Image2PyArray
    >>> i2pa = Image2PyArray()
    >>> (X_train,Y_train),(X_test, Y_test) = i2pa.from_dir("/path/to/dir");
    >>> (X_train,Y_train),(X_test, Y_test) = i2pa.from_zip("/path/to/file.zip");
    ...

Tree
-----------

+ train, testは両方必要
+ classname_1, 1.jpgなどは特に名前に制限なし
+ train, test 以下のディレクトリ名は全て一致する必要がある
+ zipでも同様に、zipのルート直下にtrain, testが両方必要

.. code-block:: pycon

    dirname
     |
     |-train
     |  |
     |  |-classname_1
     |  |  |
     |  |  |-1.jpg
     |  |  |-2.jpg
     |  |  :
     |  |  `-l.jpg
     |  |
     |  |-classname_2
     |  |  |
     |  |  |-1.jpg
     |  |  |-2.jpg
     |  |  :
     |  |  `-m.jpg
     |  :
     |  `-classname_k
     |     |
     |     |-1.jpg
     |     |-2.jpg
     |     :
     |     `-n.jpg
     | 
     `-test
        |
        |-classname_1
        |  |
        |  |-1.jpg
        |  |-2.jpg
        |  :
        |  `-p.jpg
        |
        |-classname_2
        |  |
        |  |-1.jpg
        |  |-2.jpg
        |  :
        |  `-q.jpg
        :
        `-classname_k
           |
           |-1.jpg
           |-2.jpg
           :
           `-r.jpg


機能
-----------

- directory
- zip
- (HTTP)
- (tar)

