from wagtail.blocks import ChoiceBlock, ListBlock, PageChooserBlock, StreamBlock, StructBlock, URLBlock

from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from wagtailnhsukfrontend.blocks import FlattenValueContext, CardBasicBlock, CardClickableBlock, CardFeatureBlock, CardImageBlock


class CardDocumentsBlock(CardBasicBlock):
    """
    This extends the basic card from Wagtail NHSUK Frontend package.
    A very simple card that shows a list of documents to download.
    """

    documents = ListBlock(DocumentChooserBlock(label='Documents', min_num=1, collapsed=True))

    class Meta:
        label = 'Documents card'
        icon = 'doc-full'
        template = 'blocks/card_documents_block.html'


class CardEmbedBlock(CardBasicBlock):
    """
    This extends the basic card from Wagtail NHSUK Frontend package.
    Is very similar to the CardImageBlock, but allows to embed content.
    """

    content_embed = EmbedBlock(label='Embed Url', required=True, max_height=250)
    url = URLBlock(label='URL', required=False, help_text='Optional, if there is a link the entire card will be clickable.')
    internal_page = PageChooserBlock(label="Internal Page", required=False, help_text='Optional, if there is a link the entire card will be clickable.')

    class Meta:
        label = 'Card with a video'
        icon = 'doc-full'
        template = 'blocks/card_embed_block.html'


class CardGroupBlock(FlattenValueContext, StructBlock):
    """
    This is a clone of Wagtail NHSUK Frontend package allowing to add custom cards to the CardGroupsBlock.
    """

    column = ChoiceBlock([
        ('', 'Full-width'),
        ('one-half', 'One-half'),
        ('one-third', 'One-third'),
    ], default='', required=False)

    class BodyStreamBlock(StreamBlock):
        card_basic = CardBasicBlock()
        card_clickable = CardClickableBlock()
        card_image = CardImageBlock()
        card_embed = CardEmbedBlock()  # Custom card block.
        card_documents_download = CardDocumentsBlock()  # Custom card block.
        card_feature = CardFeatureBlock()

    body = BodyStreamBlock(required=True)

    class Meta:
        icon = 'doc-full'
        template = 'wagtailnhsukfrontend/card_collection.html'
