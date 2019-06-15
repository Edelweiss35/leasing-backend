#! /usr/bin/python3
# -*- coding: utf-8 -*-




class ClauseContentReducer:
    """
    Base class used to find the clause_content
    based upon the description
    """

    def __init__(self, legal_position_preprocessor_instance,
                 xml_to_json_preprocessor_instance, *args, **kwargs):
        self.lppi = legal_position_preprocessor_instance
        self.xtjpi = xml_to_json_preprocessor_instance
        self.ngram_distribution_per_page_per_block = []
        self.locked = True

        # begin intenal method calls
        self.pages_data = self.__deduce_content_of_block__()
        self.__find_ngram_stochastic_distribution__()
        self.most_probable_blocks_in_pages = self.find_clause_name()
        self.locked = False

    def __deduce_content_of_block__(self):
        """
        Instance method used to create the paragraph of blocks
        of xml_to_json_preprocessor_instance data
        """
        data = self.xtjpi.get_JSON()
        pages_data = []
        for page in data['pages']:
            temp_page_data = {"page_number": page['page_number'],
                              "block_count": len(page['blocks']),
                              "blocks": []}
            block_counter = 0
            for block in page['blocks']:
                temp_block_data = {"id": block_counter, "content": '',
                                   "lines": block['lines'],
                                   "preprocessed_block_content": []}
                temp_block_content = ''
                for line in block['lines']:
                    if temp_block_content == "":
                        temp_block_content += line['content']
                    else:
                        temp_block_content += " %s" % line['content']
                temp_block_data['content'] = temp_block_content
                temp_block_data['preprocessed_block_content'] = self.preprocess_paragraph(temp_block_content)
                temp_page_data['blocks'].append(temp_block_data)
                block_counter += 1
            pages_data.append(temp_page_data)
        return pages_data

    def __find_ngram_stochastic_distribution__(self):
        """
        Internal Method not for external use
        used to associate the probability for finding
        ngrams of a description of lega_postion_preprocessor in the
        xml_to_json_preprocessor_instance's
        json
        """
        for page in self.pages_data:
            temp_ngram_distribution_data = {'page_number': page['page_number'],
                                            'blocks': []}
            for block in page['blocks']:
                temp_block = {'id': block['id']}

                # print("=============================================================")
                # print("blockid is ", block['id'])
                # print("block content is", block['preprocessed_block_content'])

                description_ngram_matching_factor, key_text_ngram_matching_factor = self.__find_ngram_matching_factor_in_blocks__(block['preprocessed_block_content'])
                temp_block['description_ngram_matching_probability'] = description_ngram_matching_factor
                temp_block['key_text_ngram_matching_factor'] = key_text_ngram_matching_factor
                temp_ngram_distribution_data['blocks'].append(temp_block)
                block['description_matching_probability'] = description_ngram_matching_factor
            self.ngram_distribution_per_page_per_block.append(temp_ngram_distribution_data)

    def __find_ngram_matching_factor_in_blocks__(self, preprocessed_block_content):
        """
        Internal method, not for exteranal use.
        to find the extent upto which sequences are matched
        of finding ngrams of description
        int the block and
        """
        legal_position_instance_data = self.lppi.get_data()
        temp_ngram_description_probability = []
        temp_ngram_key_text_probability = []
        for preprocessed_description in legal_position_instance_data['preprocessed_descriptions']:
            temp_ngram_description_probability_data = {'description_id': preprocessed_description['id']}
            description_ngrams = preprocessed_description['n-grams']
            preprocessed_block_ngrams = self.__create_ngram_of_preprocessed_block_content__(preprocessed_block_content, preprocessed_description['N'])
            matching_probability_of_descript_ngram_and_preprocessed_block_content_ngram = self.__find_matching_significance__(description_ngrams, preprocessed_block_ngrams)
            temp_ngram_description_probability_data['significance'] = matching_probability_of_descript_ngram_and_preprocessed_block_content_ngram
            temp_ngram_description_probability.append(temp_ngram_description_probability_data)

        for preprocessed_key_text in legal_position_instance_data['preprocessed_key_texts']:
            temp_ngram_key_text_probability_data = {'key_text_id': preprocessed_key_text['id']}
            key_text_ngrams = preprocessed_key_text['n-grams']
            preprocessed_block_ngrams = self.__create_ngram_of_preprocessed_block_content__(preprocessed_block_content, preprocessed_key_text['N'])
            matching_probability_of_key_text_ngram_and_preprocessed_block_content_ngram = self.__find_matching_significance__(key_text_ngrams, preprocessed_block_ngrams)
            temp_ngram_key_text_probability_data['significance'] = matching_probability_of_key_text_ngram_and_preprocessed_block_content_ngram
            temp_ngram_key_text_probability.append(temp_ngram_key_text_probability_data)
        return (temp_ngram_description_probability, temp_ngram_key_text_probability)

    def __create_ngram_of_preprocessed_block_content__(self, preprocessed_block_content, N):
        """
        Intenal Method not for external use.just used to create the N-grams of the
        preprocessed_block_content from XML_to_JSONpreprocessor instance
        """
        ngrams_to_return = []
        for n in range(1, N+1):
            grams = ngrams(list(filter(None, preprocessed_block_content)), n)
            for gram in grams:
                ngrams_to_return.append(gram)
        return ngrams_to_return

    def __find_matching_significance__(self,
                                       input_ngrams,
                                       preprocessed_block_ngrams):
        """
        Interanl/private method not for external use.
        should be called by any other class method
        it find the significane of finding POS1 arg
        ngrams in POS2 arg ngrams.
        both POS1 arg and POS2 args are ngram lists
        """
        return_significance = 0
        ngram_union = set(input_ngrams).intersection(set(preprocessed_block_ngrams))
        for ngram in ngram_union:
            return_significance += log(len(ngram) + 1)
        return return_significance

    def find_clause_name(self):
        """
        method used to find the clause name 
        using the instance's ngram_distribution_per_page_per_block
        and instance's pages_data variables
        """
        most_probable_blocks_in_pages = []
        for page in self.ngram_distribution_per_page_per_block:
            temp_page_data = {"page_number": page["page_number"], "blocks":[]}
            for block in page['blocks']:
                temp_block_data = {"id": block['id'],
                                   "key_text_ngram_matching_factors": [],
                                   "description_ngram_mathching_factors": []
                }
                combined_key_text_matching_significance = 0
                combined_description_matching_significance = 0

                for key_text_ngram_matching_factor in block["key_text_ngram_matching_factor"]:
                    temp_block_data["key_text_ngram_matching_factors"].append(key_text_ngram_matching_factor)
                    combined_key_text_matching_significance += key_text_ngram_matching_factor["significance"]

                for description_ngram_matching_probability in block["description_ngram_matching_probability"]:
                    temp_block_data["description_ngram_mathching_factors"].append(description_ngram_matching_probability)
                    combined_description_matching_significance += key_text_ngram_matching_factor["significance"]

                average_key_text_matching_factor = combined_key_text_matching_significance / len(block["key_text_ngram_matching_factor"])
                average_description_matching_factor = combined_description_matching_significance / len(block["description_ngram_matching_probability"])

                if(average_description_matching_factor) > 0 and (average_key_text_matching_factor > 0):
                    # parse the self.page_data
                    # for the same page number and same block id
                    # line by line and check try to find the clause name
                    temp_block_data["average_key_text_matching_factor"] = average_key_text_matching_factor
                    temp_block_data[average_description_matching_factor] = average_description_matching_factor
                    temp_block_data["combined_key_text_description_average_matching_factor"] = (average_description_matching_factor + average_key_text_matching_factor) / 2
                    for _page in self.pages_data:
                        if _page['page_number'] == page['page_number']:
                            for _block in _page['blocks']:
                                if _block['id'] == block['id']:
                                    pass
                                    # temp_block_data["lines"] = _block["lines"]
                    temp_page_data['blocks'].append(temp_block_data)
            if(len(temp_page_data['blocks']) > 0):
                most_probable_blocks_in_pages.append(temp_page_data)
        for page in most_probable_blocks_in_pages:
            cumulative_average_of_all_blocks = 0
            for block in page["blocks"]:
                cumulative_average_of_all_blocks += block["combined_key_text_description_average_matching_factor"]
            average_cumulative_average_of_all_blocks = cumulative_average_of_all_blocks / len(page['blocks'])
            page["average_cumulative_average_of_all_blocks"] = average_cumulative_average_of_all_blocks
        return  most_probable_blocks_in_pages

    def preprocess_paragraph(self, block_content):
        """
        Instance method used to preprocess
        the block content or the paragraph
        for futher NLP operations
        """

        block_content = block_content
        tokens = word_tokenize(block_content)
        lem = WordNetLemmatizer()
        stop_words = set(stopwords.words("english"))
        # leminizing
        return [lem.lemmatize(w.encode('ascii', 'ignore').decode("utf-8")).lower() for w in tokens if((not w in stop_words) and (not w in string.punctuation) and (len(w) > 0))]

    def get_JSON(self):
        """
        Mthod used to return the
        instance pages_data on if instance variable locked
        is False
        """
        if not self.locked:
            return (self.ngram_distribution_per_page_per_block, self.pages_data, self.most_probable_blocks_in_pages)
        else:
            raise Exception("%s class instance is still under processing. please hold untill lock is released")
