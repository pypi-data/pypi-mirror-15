Python Library for Juspay Express Checkout API


Installation


Prerequisites:

    Ensure that you have installed the 'requests' package for python,

    If not, open the terminal and type 'pip install requests'

    NOTE: If pip is not installed, install pip by download get_pip.py from the https://bootstrap.pypa.io/get-pip.py and
    run the script in your terminal

Procedure

    Run the following command in your terminal

        pip install JuspayECLibrary

    You can use the library by including the following import statement in your python script
        import JuspayECLibrary.ECLib as ECLib

    Now, you can use the library as follows

        ECLib.api_key = 'your_api_key'
        ECLib.Orders.create(order_id=1,amount=100.0)

For more instructions on how to use the library, please refer to the documentation at https://apidocs.juspay.in

