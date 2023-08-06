================
Django Timelines
================

This provides a back-end for `Timelines JS 3`_. You can use external links to media
or link to internal objects.

.. _Timelines JS 3: http://timeline.knightlab.com/docs/index.html

Initial Setup
=============

1. Install it via ``pip``::

      pip install django-timelines

2. Modify ``INSTALLED_APPS``::

      INSTALLED_APPS = [
          ...
          "contentrelations",
          "timelines",
      ]

3. Set ``TIMELINES_BACKGROUND_IMAGE_MODEL`` setting before you migrate the app. This model should be a photo management application that you use. This setting allows ``swapper`` to set up the relationship between that model and the ``timelines`` models::

      TIMELINES_BACKGROUND_IMAGE_MODEL = "media.Photo"

4. Set ``TIMELINES_SETTINGS``. The ``BACKGROUND_IMAGE_RELATED_FIELD`` is the actual ``FileField`` or ``ImageField`` on the ``TIMELINES_BACKGROUND_IMAGE_MODEL``::

      TIMELINES_SETTINGS = {
          'BACKGROUND_IMAGE_RELATED_FIELD': 'photo',
      }


Creating Adapters
=================

In order to use an existing model in your timelines, you need to create an adapter for it. The adapter allows you to customize or map the information required by Django Timelines to your model. A couple of notes about adapters:

* The adapter for a model **does not** need to be in the same application as the model. This allows you to adapt models installed via ``pip`` and which you have no control.
* Django Timelines will import the ``adapters`` module for every installed application at startup. That's a good place to put your adapters.

Adapter Example
---------------

::

   from timelines.registration import registry, TimelineAdapter
   from .models import Photo


   class PhotoAdapter(TimelineAdapter):
       def get_headline(self):
           return self.instance.title

       def get_clickthrough_url(self):
           return self.instance.get_absolute_url()

       def get_credit(self):
           return self.instance.taken_by

       def get_text(self):
           return self.instance.description

       def get_media_url(self):
           return self.instance.photo.url

       def get_thumbnail(self):
           return self.instance.photo.url

   registry.register(Photo, PhotoAdapter)

Using adapters
--------------

Adapters define several attributes and their accessor methods.

* ``clickthrough_url`` and ``get_clickthrough_url()``: a URL that, if provided, adds a "READ MORE" link to the description. Return `None` to omit link.
* ``credit`` and ``get_credit()``: the credit information for the media provided.
* ``headline`` and ``get_headline()``: the headline for the slide.
* ``media_url`` and ``get_media_url()``: the URL to the media for the slide.
* ``text`` and ``get_text()``: the text of the slide.
* ``thumbnail`` and ``get_thumbnail()``: a thumbnail for the timeline

To minimize the amount of work you have to do, the adapter is smart enough to look for the attribute name on the model instance. Instead of ``adapter.get_headline()`` you should just use ``adapter.headline`` so the adapter can use its internal logic to get the correct value.

When you access one of the required attributes, the adapter first tries the ``get_FOO()`` method. If the value returned is "falsey"_, then the adapter looks for the attribute on the model instance. So if your model already has a ``text`` attribute, you do not need to define a ``get_text`` method unless you wish to modify the value.

.. _"falsey": https://docs.python.org/2.7/library/stdtypes.html#truth-value-testing

Defining media for a Timeline or Slide
======================================

Both Slides and Timelines (for the title slide) define a piece of media to show on the slide. Django Timelines allows either the specifying of an external URL or a link to an internal object. The benefit of an internal object link, is that it can provide the values for the other fields for you, and modifications of the object automatically appear on the timeline.

Even if you specify an internal object, you can still override the values provided by that model's adapter.

1. Specify the media:

   * For external URLs, simply enter the value in the **Media URL** field.
   * For internal objects, select the model from the **Media content type** field (only models with registered adapters are shown). Then click on the magnifying glass icon to open a window to browse for an object. You can also create a new object on the fly here.

2. Set the content fields:

   * For external URLs, you must set appropriate values manually.
   * For interal objects, the help text under each of the fields will tell you the default as determined from the model's adapter. You only need to enter values if necessary.

3. Modify the background *(optional)*

   * Click **Use media as background** to use the URL or object specified in #1 as the background for the slide.
   * You can specify an alternative image to use as the background by specifying a **Background image**.
   * You can specify a color for the background (default is white).

Creating a Timeline
===================

1. Follow the instructions above in `Defining media for a Timeline or Slide`_ to specify the title slide information and background.
2. In the **Other Information** section, you can alter the **Scale**, add **Eras** (see Eras_ below) and mark the Timeline as **Published**.

Adding slides to a Timeline
---------------------------

1. Click on **Add another Slide**.
2. Click on the magnifying glass icon.
3. Select or create a slide. Once you have saved the Timeline, you will see summary data about the slide and a link to edit the slide.
4. TimelineJS has the ability to organize events in the same row or adjecent rows based on their **group**. You can fill in the group attribute if necessary.
5. Enter in the **Order** if necessary. Slides are automatically sorted by their date. However, since several events could have the same date, use the order field for fine control over them.

Creating a Slide
================

1. Set a start date and optional time. See `Dates, times and resolution`_ below for more information regarding dates.
2. Optionally set an end date and time.
3. Set the media and content according to `Defining media for a Timeline or Slide`_ above.

Dates, times and resolution
---------------------------

You can specify a date with variable resolution. The allowed resolutions are:

* **Year** (e.g. 1776)
* **Month** (e.g. July 1776)
* **Date** (e.g. July 4, 1776)
* **Datetime** (e.g. July 4, 1776 at 5:24 PM)

Dates are sorted from lowest resolution to heighest resolution, in that:

* Year resolution is sorted before January 1 of the same year. Consider it January 0th of that year.
* Month resolution is sorted before the 1st of the month of that year. Consider it the 0th of the specified month.
* Date resolution is sorted before Midnight of that date. Consider it the -1 AM of that date, since Midnight is 0.
* Datetime resolution is sorted according to the time.

Eras
====

Eras are used to label a span of time on the timeline navigation component. Eras are reusable across Timeline objects. They consist of a start and end date and an optional label.


