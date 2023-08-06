.. :changelog:

History
-------
0.2.0 (2016-06-18)
++++++++++++++++++
* Rename: `views.py` to `mixins.py` because is the propper name
* Add: `boilerplate.py` with the default settings, you can customize your error messages. 
* Add: `forms.py` Forms with validation to the following Views:
* Add: `views.py`: `LoginView`
* Add: `views.py`: `RecoverAccountView`
* Add: `views.py`: `RegistrationView`
* Add: `views.py`: `LoginView`

0.1.3 (2016-06-16)
++++++++++++++++++
* Fix: CRUD Messages Mixin conflict with Extra Forms and Formsets Mixin
* Fix: ExtraFormsandFormsetsMixin validate if `formset_list` or `extra_form_list` exists
* Fix: App template tags, didn't got the model information intead of the app information


0.1.0 (2016-06-12)
++++++++++++++++++
* Fix: CRUD Messages Mixin
* Bug: Variables got reasigned ExtraFormsAndFormsetsMixin on the get_context_data
* Convert spaces to tabs

0.0.1 (2016-06-6)
++++++++++++++++++
* project added