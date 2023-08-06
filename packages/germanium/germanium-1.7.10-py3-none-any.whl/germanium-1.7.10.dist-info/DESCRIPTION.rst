germanium
=========

Germanium is a set of extensions on top of the regular WebDriver API, allowing
for a super easy creation of tests. It's opensource and free.

Simply put Germanium is a Web Testing API that doesn't disappoint::

    from germanium.static import *
    from time import sleep

    open_browser("ff")
    go_to("http://www.google.com")
    type_keys("germanium pypy<enter>", Input("q"))
    wait(Link("Python Package Index"))
    click(Link("Python Package Index"))
    sleep(5)
    close_browser()


Here is the usage documentation: [germanium-usage.pdf](https://raw.githubusercontent.com/germaniumhq/germanium/master/doc/out/germanium-usage.pdf)



