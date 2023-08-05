# bsw
bsw - Build Static Website, a simple static website generator.


## Usage (the short version)

```
usage: bsw.py [-h] [-C] [-s]

bsw - build static website

optional arguments:
    -h, --help         show this help message and exit
    -C, --clean        remove existing build folder before building
    -s, --http-server  serve content after build (default port 8000)
```

Nice and simple.

## Getting Started

bsw works on the current directory, and expects a couple of
folders to exist:

* pages
* templates

To get started, we'll need to create these folders and add a base
template (the primary site template) to the *templates* folder.

```
$ mkdir pages
$ mkdir templates
$ echo <<EOF > templates/base.html
> <html>
> <head><title>\$page_title</title></head>
> <body>
> \$page_content
> </body>
> </html>
> EOF
```

bsw will read all the \*.html and \*.htm files inside the `pages` directory
(recursively) and render them using the base template. The rendered pages
will then be saved to the `build` folder (which will be created if needed).

Template placeholders (e.g. `$page_title`) are replaced with page variables
from the page content file. These are declared like
`<!-- page_title = "my page title" -->`.

The special `$page_content` placeholder is replaced with the page content
itself (the body of the `pages/*.html` file).

Let's create an example page:

```
$ mkdir pages/about
$ echo <<EOF > pages/about/index.html
> <!-- page_title = "about this site" -->
> <h1>About this site</h1>
> <p>This is our example site, built with bsw.</p>
> EOF
```

Creating the page at `pages/about/index.html` allows us to 
access the page using the pretty URL `/about` (rather than `about.html`).

Now that we have some sample content, we can build the website:

```
$ bsw.py -s
```

The `-s` flag tells bsw to start a web server on port 8000 after building
the site. We can then access our about page via
<a href="http://localhost:8000/about">http://localhost:8000/about</a>.


## Static content

bsw will copy any files in `static/` and `templates/static/` to
to the combined `build/static/` folder where they can easily be
referenced by your page or template content. For example, include
the `templates/static/logo.png` file on your template or page as
so: `<img src="/static/logo.png">`.

Static folders are completely optional and both template and site
statics are accessed from the same combined folder.


## Includes

You can include reusable pieces of markup by using *include* directives.

You must place all includes in `templates/includes/`.

For example, let's create an include with a link to the bsw project
repository on GitHub:

```
$ mkdir templates/includes
$ echo <<EOF > templates/include/github_links.html
> <p>
> <a href="https://github.com/davb5/bsw">github.com/davb5/bsw</a>
> </p>
> EOF
```

We can now reference this include from any of our page or template
files by adding the following directive to the page markup:


```
<!-- include("github_links.html") -->
```


# FAQ

## Why are there two static folders?

`bsw` looks for two static folders:

* static/
* templates/static/

This allows you to keep your template static files separate from your
page static files, making it easier to reuse your template on other sites.

However, the use of either (or both) static folders is completely optional.


## How do I create a template?

Templates are extemely simple. The default template for any page which doesn't
explicitly specify a template is `templates/base.html`.

It requires only a single tag:

```
$page_content
```

The content from each .html or .htm file in `pages/` is inserted into the
base template at the `$page_content` tag.

Pages can also pass values to the template, for example, you template could
contain the following:

```
<head>
    <title>My Example Blog | $page_title</title>
</head>
```

You can populate the `$page_title` variable for any page by declaring it
in a comment in the page markup, as follows:

```
<!-- page_title = "My first blog post! -->
```

*The only template tag which is required is the `$page_content` tag.*


## How do I use multiple templates?

Additional templates can be created in the `templates` folder and referenced
from pages by using the special `template` page variable as so:
`<!-- template = "my_special_case_template.html" -->`

The `<!-- template ... -->` variable can appear anywhere in the page content (it
doesn't need to be placed at the top of the file).

Any page which doesn't explicitly specify a template will use the *base template*
`templates/base.html`.
