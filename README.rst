This package is an interface to the Arecibo application from ClearWind. It 
provides an interface for Plone to report its errors. 

This is the version that is updated for use with Plone 4 and has not been 
tested with previous versions but is likely to work with Plone 3 as well. It 
also adds generic setup support and support for complete configuration from 
the control panel.


For more information see: http://areciboapp.com and specifically 
http://www.areciboapp.com/docs/plone/   

Configuration
-------------

Configuration has moved from arecibo.xml to plone.app.registry's registry.xml.

To configure to clearwind.arecibo's via your add-on package, add a 
``registry.xml`` file to your package's installation profile 
(typically profiles/default). 

Your ``registry.xml`` file should look something like this:

::

    <?xml version="1.0"?>
    <registry>
        <records interface="clearwind.arecibo.interfaces.IAreciboConfiguration">
            <value key="account_number">12345</value>
            <value key="app_name">my_app</value>
            <value key="transport">http</value>
            <value key="ignore_localhost">True</value>
        </records>
    </registry>
