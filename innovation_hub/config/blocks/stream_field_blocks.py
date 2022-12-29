from wagtail.core import blocks


class VerticalStepperBlock(blocks.StructBlock):
    """Cards with image and text and button(s)."""

    steps = blocks.ListBlock(
        blocks.StructBlock([
            ("title", blocks.CharBlock(required=True, max_length=100)),
            ("text", blocks.TextBlock(required=True))
        ])
    )

    class Meta:
        template = "blocks/step_block.html"
        icon = "placeholder"
        label = "Vertical stepper"
