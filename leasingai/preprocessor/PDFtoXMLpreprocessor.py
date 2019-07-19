


class PDFtoXML:
    """
    class used to convet the pdf file
    saved in uploaded doucment model
    to an XML structure
    and that structure can be saved to database also
    """
    def __init__(self, doucment_id):
        """
        constructor of the class
        used to initialize following instance variables

        > doucment_instance : Django Model instance reacord object
        > XML_string : String
        > XML_dict : dict
        > safe_to_query : Boolean
        > temp_doucment_file : NamedTemporaryFile instance
        > number_of_pages : Number instance

        saving PDF content to temp_doucment_file
        finding number of pages and initiating it
        to number_of_pages instance variable

        finally it call the parse method that
        initiate the further parsing of data
        and update the XML_string variable along parsing
        """

        self.document_instance = DocumentUpload.objects.get(id=doucment_id)
        self.XML_string = str()
        self.XML_dict = dict()
        self.safe_to_query = False
        self.parent_XML = etree.parse(io.StringIO('<?xml version="1.0" ?><doc></doc>'))

        # create a named temporary
        # file of uploaded document
        self.temp_doucment_file = NamedTemporaryFile(suffix=".pdf",
                                                     delete=False)

        # saving the data of uploaded doucment to named
        # temporary file
        with open(self.temp_doucment_file.name, 'wb') as writeto:
            writeto.write(self.document_instance.document.read())

        # initialize the number of pages in PDF file
        # to instance variable and call the parse Method
        # to parse the PDF to XML string
        self.number_of_pages = self.find_number_of_pages()
        self.parse()

    def find_number_of_pages(self):
        """
        instance method used to find the number of pages in the pdf file
        associated with the doucment ID provided to the class constructor
        """

        pdf = PdfFileReader(open(self.temp_doucment_file.name, 'rb'))
        return pdf.getNumPages()

    def parse(self):
        """
        Method used to initiate the parsing after the temp_doucment_file
        is created for parsing
        """
        
        def __parse_page(page_no):
            """
            clousre to parse a particular page and
            and update the XML_string instance vaiable with the string
            """

            pdftotext_cli_string  = "pdftotext -f %s -bbox-layout %s -" % (page_no, self.temp_doucment_file.name)  # NOQA
            print("PDFtoXML query_string is", pdftotext_cli_string)
            subprocess_args = split(pdftotext_cli_string)
            process = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            # communicate with process to get output and errors
            (output, errors) = process.communicate()

            # save the data if there is no
            # error else raise Exception
            if not errors:
                current_page_xmlelement = etree.parse(io.BytesIO(output)).xpath('/*/*[2]/*/*[1]') # it will return a list of all matched elements
                current_page_xmlelement[0].attrib['page_no'] = str(page_no)
                return current_page_xmlelement[0]
            else:
                raise Exception(errors)

        def __parse_page_range(initial, final):
            """
            clousre used to parse the pages in range it run a for loop
            to calll __parse_page and save the data in dictionary format
            page_no as a key
            """
    
            for page_no in range(initial, final):
                self.XML_dict[page_no] = __parse_page(page_no)
                self.parent_XML.getroot().append(self.XML_dict[page_no])


        # find the half value of the total number of pages and divide them
        # into four groups run each group in a thread to reduce the processng
        # time
        number_of_pages_per_thread = self.number_of_pages // 4
        thread_1 = threading.Thread(target=__parse_page_range,
                                    args=(1,
                                          number_of_pages_per_thread + 1))
        thread_2 = threading.Thread(target=__parse_page_range,
                                    args=(number_of_pages_per_thread + 1,
                                          2*(number_of_pages_per_thread + 1)))
        thread_3 = threading.Thread(target=__parse_page_range,
                                    args=(2*(number_of_pages_per_thread + 1),
                                          3*(number_of_pages_per_thread + 1)))
        thread_4 = threading.Thread(target=__parse_page_range,
                                    args=(3*(number_of_pages_per_thread + 1),
                                          (self.number_of_pages + 1)))

        # starting threads
        thread_1.start()
        thread_2.start()
        thread_3.start()
        thread_4.start()

        # wait untill threads are executed
        thread_1.join()
        thread_2.join()
        thread_3.join()
        thread_4.join()

        # After all threads are executed it is safe_to_query
        # now so we are setting safe_to_query instance variable
        # to true
        self.safe_to_query = True
        # remove temp document file created initaially
        self.remove_temp_document_file()

    def remove_temp_document_file(self):
        """
        function used to removed the named temporary
        file created to save the PDF file in database
        """
        os.remove(self.temp_doucment_file.name)

    def create_valid_XML_object(self):
        if self.safe_to_query:
            return self.parent_XML 
        else:
            return Exception("Threads are still running and parsing the file. Please wait untill all threads are completed")  # NOQA
