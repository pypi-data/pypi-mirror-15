Wagtail Table Block
===================

Don't use this if you can help it. Wagtail 1.5 features [this exact code](https://github.com/torchbox/wagtail/pull/1705) merged into Wagtail's core. This exists only as an intermittent solution before Wagtail 1.5 is released, and perhaps as a way to quickly include the table block in a project with Wagtail < 1.5.

Since the code is identical to the code in core, the database representation and is the same. Therefore you can remove this plugin and simply change your imports once you upgrade to Wagtail 1.5.

Install with

    pip install wagtail-table-block

Then add `wagtail_table_block` to your `INSTALLED_APPS`.

Then use `from wagtail_table_block.fields import TableBlock` and implement it like `table = TableBlock()`.


