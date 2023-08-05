bsw
===

bsw - Build Static Website, a simple static website generator.

Usage (the short version)
-------------------------

::

    usage: bsw_run.py [-h] [-C] [-s] [--init [PATH]] [--template TEMPLATE]
    
    bsw - build static website
    
    optional arguments:
      -h, --help           show this help message and exit
      -C, --clean          remove existing build folder before building
      -s, --serve          serve content after build (default port 8000)
      --init [PATH]        initialise a new bsw site as the specified path
      --template TEMPLATE  built-in template to use with --init

Nice and simple.

Getting Started
---------------

bsw works on the current directory, and expects a couple of folders to
exist:

-  pages
-  templates

To get started, we'll need to create these folders and add a base
template (the primary site template) to the *templates* folder.

::

    $ bsw --init mynewsite
    $ cd mynewsite
    $ bsw --serve

Open <a href="http://localhost:8000/about">http://localhost:8000/about</a>
in your browser and you'll see your new site, ready to go.

bsw will read all the \*.html and \*.htm files inside the `pages` directory
(recursively) and render them using the templates in the templates folder
(using base.html by default if a page doesn't have a template directive).
The rendered pages will then be saved to the `build` folder (which will be
created if needed).

Variables in page (e.g. ``<!-- page_title = "my page title" -->``) are placed
into the templates at the placeholders (e.g. ``$page_title``). It's easy to 
add your own, and you can see a great example of this in the sample blog
template and blog post.

The best way to learn the syntax is to take a look at the example pages
and templates. They're purposefully very simple and should be easy to
pick up.

Static content
--------------

bsw will copy any files in ``static/`` and ``templates/static/`` to to
the combined ``build/static/`` folder where they can easily be
referenced by your page or template content. For example, reference the
``templates/static/logo.png`` file on your template or page as so:
``<img src="/static/logo.png">``.

Static folders are completely optional and both template and site
statics are accessed from the same combined folder.

Includes
--------

You can include reusable pieces of markup by using *include* directives.

You must place all includes in ``templates/includes/``.

For example, let's create an include with a link to the bsw project
repository on GitHub:

::

    $ mkdir templates/includes
    $ echo <<EOF > templates/include/github_links.html
    > <p>
    > <a href="https://github.com/davb5/bsw">github.com/davb5/bsw</a>
    > </p>
    > EOF

We can now reference this include from any of our page or template files
by adding the following directive to the page markup:

::

    <!-- include("github_links.html") -->

FAQ
===

Why are there two static folders?
---------------------------------

``bsw`` looks for two static folders:

-  static/
-  templates/static/

This allows you to keep your template static files separate from your
page static files, making it easier to reuse your template on other
sites.

However, the use of either (or both) static folders is completely
optional.

How do I create a template?
---------------------------

Templates are extemely simple. The default template for any page which
doesn't explicitly specify a template is ``templates/base.html``.

It requires only a single tag:

::

    $page_content

The content from each .html or .htm file in ``pages/`` is inserted into
the base template at the ``$page_content`` tag.

Pages can also pass values to the template, for example, you template
could contain the following:

::

    <head>
        <title>My Example Blog | $page_title</title>
    </head>

You can populate the ``$page_title`` variable for any page by declaring
it in a comment in the page markup, as follows:

::

    <!-- page_title = "My first blog post! -->

*The only template tag which is required is the ``$page_content`` tag.*

How do I use multiple templates?
--------------------------------

Additional templates can be created in the ``templates`` folder and
referenced from pages by using the special ``template`` page variable as
so: ``<!-- template = "my_special_case_template.html" -->``

The ``<!-- template ... -->`` variable can appear anywhere in the page
content (it doesn't need to be placed at the top of the file).

Any page which doesn't explicitly specify a template will use the *base
template* ``templates/base.html``.

How do I deploy my site?
------------------------

Your hosting environment will vary, but deployment is as simple as copying
the contents of the build folder to somewhere accessible on your web server.

Popular workflows include using rsync (copying only files which have changes)
or git (handy if you already keep the site source content in a git repository).
