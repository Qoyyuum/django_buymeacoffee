Django-BuyMeACoffee
===================

[![Upload Python Package](https://github.com/Qoyyuum/django_buymeacoffee/actions/workflows/python-publish.yml/badge.svg?branch=main)](https://github.com/Qoyyuum/django_buymeacoffee/actions/workflows/python-publish.yml)

Django-BuyMeACoffee is a Django application that integrates the Buy Me A Coffee API into your Django project. The app provides a simple way to create a Buy Me A Coffee page and accept donations from users.

The app provides the following features:

* A simple API client to interact with the Buy Me A Coffee API
* A model to store the donations
* A view to display the donations
* A template to display the Buy Me A Coffee page

With Django-BuyMeACoffee, you can easily add a Buy Me A Coffee page to your Django project and start accepting donations from users. This is a great way to monetize your open source project or to support your content creation.

The app is easy to use and requires minimal setup. You can have a Buy Me A Coffee page up and running in minutes.

Installation Guide
==================

Follow these steps to integrate Django-BuyMeACoffee into your Django project:

1. **Install the Package**  
   Run the following command to install the package via pip:
   ```
   pip install django-buymeacoffee
   ```

2. **Add to Installed Apps**  
   Include `django_buymeacoffee` in your `INSTALLED_APPS` setting in `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...,
       'django_buymeacoffee',
   ]
   ```

3. **Configure URLs**  
   Add the app's URLs to your project's `urls.py`:
   ```python
   from django.urls import path, include

   urlpatterns = [
       ...,
       path('buymeacoffee/', include('django_buymeacoffee.api.urls')),
   ]
   ```

4. **Run Migrations**  
   Apply the database migrations for the app:
   ```
   python manage.py migrate django_buymeacoffee
   ```

5. **Set Up Webhook URL**  
   Ensure that your webhook URL is correctly configured to receive events from Buy Me A Coffee. This typically involves setting the `webhook_url` in your environment or settings.

6. **Configure Buy Me A Coffee API**  
   Set up your Buy Me A Coffee API credentials in your project's settings, which might include API keys or tokens.

7. **Verify Installation**  
   Once set up, verify the integration by navigating to the Buy Me A Coffee page on your site and testing the donation features.

Your Django project is now ready to accept donations using the Buy Me A Coffee integration!

The app is open source and available on GitHub. Feel free to contribute to the project or report any issues you may encounter.

.. image:: https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=qoyyuum&button_colour=5F7FFF&font_colour=ffffff&font_family=Lato&outline_colour=000000&coffee_colour=FFDD00
   :target: https://buymeacoffee.com/qoyyuum
