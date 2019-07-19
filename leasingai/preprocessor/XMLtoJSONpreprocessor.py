

class Word:
    """
    Abstract representation of each word tag in the XML bbox-layout
    of PDF file
    """

    def __init__(self, XML_word_element, *args, **kwargs):
        self.XML_word_element = XML_word_element
        self.sanitized_value = ''
        self.lock = True

        # initiate parsing to find the inner text of
        # word tag .Actually each word in the PDF file is
        # enclosed in the <word> tag of XML bbox-layout
        # and each word in PDF should be inner text of
        # some <word> tag in XML
        self.__find_inner_text()

    def __find_inner_text(self):
        """
        Internal method used to find the sanitized
        inner text of the word tag. for sanitization
        a closure named sanitized_inner_text is used for that
        """

        def sanitized_inner_text(inner_text):
            """
            closure used to sanitized the text
            provided to it. 
            > It is responsible for removing additional space
              before and after of the word
            > remove escape sequences like \n
            """
            return inner_text.strip()

        # initializing the sanitized value instance variable with the sanitized
        # inner text of XML_word_element instance variable
        self.sanitized_value = sanitized_inner_text(self.XML_word_element.text)

        # only usefull if Class is initiated
        # asynchronously, in our case there is not
        # need of this . But still to be more azile
        # for future this thing is kept here
        self.lock = False

    def get_sanitized_value(self):
        """
        Instance Method used to return the sanitized_value
        instance variable only if lock is False.
        """
        if not self.lock:
            return self.sanitized_value
        else:
            raise Exception("%s class is still under processing. Please wait untill the lock is released")


class Line:
    """
    abstract representation of each line in the line in the XML 
    bbox-layout of PDF file
    """
    def __init__(self, XML_line_element, *args, **kwargs):
        self.XML_line_element = XML_line_element
        self.JSON = {'words': [], 'content': ''}
        self.lock = True

        # Calling the parser
        self.__parse_line_to_JSON()

    def __create_word_children_iterator(self):
        """
        Internal method used to retun all iterator
        object containg all the siblings of XML_line_element
        that have tag name word
        """
        return self.XML_line_element.getiterator(tag='{http://www.w3.org/1999/xhtml}word')

    def __parse_line_to_JSON(self):
        """
        Internal method used to fill the values in
        self.JSON dictionary with the words and content 
        """
        # updating the self.JSON instance variable with words
        # element inner text  using the word class
        for word_element in self.__create_word_children_iterator():
            _word = Word(word_element)
            self.JSON['words'].append(_word.get_sanitized_value())
        self.JSON['content'] = " ".join(self.JSON['words'])

        # the line below will remove the unicode chars form the words and also stop words and punctuations
        # this block is intensionaly kept here as we will
        lem = WordNetLemmatizer()
        stop_words = set(stopwords.words("english"))
        self.JSON['words'] = [lem.lemmatize(w.encode('ascii', 'ignore').decode("utf-8")).lower() for w in self.JSON['words'] if((w not in stop_words) and (w not in string.punctuation) and (len(w) > 0))]
        # only usefull if Class is initiated
        # asynchronously, in our case there is not
        # need of this . But still to be more azile
        # for future this thing is kept here
        self.lock = False

    def get_JSON(self):
        """
        Method used to return the JSON representation of the 
        line in form of a Dictionary
        """
        if not self.lock:
            return self.JSON
        else:
            raise Exception("%s class instance is still under processing. Please wait untill lock is released" % self.__class__.__name__)


class Block:
    """
    Abstract representation of every block element
    in the bbox-layout of the PDF file's respective HTML
    file
    """

    def __init__(self, XML_block_element, *args, **kwargs):
        self.XML_block_element = XML_block_element
        self.JSON = {'lines': [], 'type': 'block'}
        self.lock = True

        # Begin Parsing
        self.__parse_block_to_JSON()

    def __create_line_children_iterator(self):
        """
        Internal Method used to return the iterator
        of all Line tags siblings of Block tag in the
        XML bbox-layout of PDF file
        """
        return self.XML_block_element.getiterator(tag='{http://www.w3.org/1999/xhtml}line')

    def __parse_block_to_JSON(self):
        """
        Internal Method used to convert the XML Block element 
        to JSON representation. This methos also create 
        Line class instance for the line subelement inside
        the block element in  bbox-layout of PDF file
        """
        # upating the self.JSON instance variable with the
        # JSON representation of its line siblings
        for line_element in self.__create_line_children_iterator():
            _line = Line(line_element)
            self.JSON['lines'].append(_line.get_JSON())

        # only usefull if Class is initiated
        # asynchronously, in our case there is not
        # need of this . But still to be more azile
        # for future this thing is kept here
        self.lock = False

    def get_JSON(self):
        """
        funtion that return the JSON representation
        of the XML block element in form of Python Dictionary
        """
        if not self.lock:
            return self.JSON
        else:
            raise Exception("%s class instance is still processing some elements. Please wait untill Lock is released" % self.__class__.__name__)


class Page:
    """
    This class is abstract representation of each
    page element in the XML file that represent the bbox-layot of 
    PDF files
    """

    def __init__(self, XML_page_element, *args, **kwargs):
        self.XML_page_element = XML_page_element
        self.JSON = {'blocks': [], 'type': 'page'}
        self.lock = True

        # begin parsing
        self.__parse_page_to_JSON()

    def __create_block_children_iterator(self):
        """
        Internal Mehod used to return the iterator
        object of all siblings of page that have
        tag name block
        """
        return self.XML_page_element.getiterator(tag='{http://www.w3.org/1999/xhtml}block')

    def __parse_page_to_JSON(self):
        """
        Internal Method used to parse the Page XML Element
        and converty it to JSON representation. it create a Block
        class instance for each block in the XML.
        """
        self.JSON['page_number'] = self.XML_page_element.attrib['page_no']

        # call create Block class instance for each
        # Block tag child element of instance's XML_page_element
        for block  in self.__create_block_children_iterator():
            _block = Block(block)
            self.JSON['blocks'].append(_block.get_JSON())
        self.lock = False

    def get_JSON(self):
        """
        Method used to return the JSON
        representation of Page XML element
        """
        if not self.lock:
            return self.JSON
        else:
            raise Exception("%s class instance is still processing XML element. Please wait while the lock is released" % self.__class__.__name__)


class BboxXMLParser:
    """
    Base class to convert the XML bbox-layout
    of the PDF file the JSON representation
    which will in form:

    output JSON  : {pages: [{blocks: [{lines: [{words: ['string', 'string'], content: 'string'}, {}, {}}, ...] }, {}, {}...] }, {}, {}...]}
    """

    def __init__(self, XMLtoPDF_instance, *args, **kwargs):
        self.XMLtoPDF_instance = XMLtoPDF_instance
        self.JSON = {'pages': [], 'count': 0}
        self.lock = True

        # begining XML to JSON Conversion
        self.__XMLtoJSON()

    def __XMLtoJSON(self):
        """
        Internal Method used to initiate the parsing of the XML doucment
        its main task is to get all of the page element form the XML_to_PDF_instance
        and call the 
        """

        xml_etree = self.XMLtoPDF_instance.create_valid_XML_object()
        doc = xml_etree.getroot()
        pages = doc.getchildren()

        # set the count key of self.JSON
        self.JSON['count'] = len(pages)

        # call create page class instance for each
        # Page tag child element of the doc
        for page in pages:
            print("page is ", page)
            _page = Page(page)
            self.JSON['pages'].append(_page.get_JSON())

        # only usefull if Class is initiated
        # asynchronously, in our case there is not
        # need of this . But still to be more azile
        # for future this thing is kept here
        self.lock = False

    def get_JSON(self):
        """
        methos used to return a dictiionary that represent the whole
        bbox-layout of PDF file in form of a dictionary
        """
        if not self.lock:
            return self.JSON
        else:
            raise Exception("%s instance is still locked. It is still processing. Please wait utill unlocked"  % self.__class__.__name__)
