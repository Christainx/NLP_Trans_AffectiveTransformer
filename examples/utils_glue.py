# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors and The HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" BERT classification fine-tuning: utilities to work with GLUE tasks """

from __future__ import absolute_import, division, print_function

import csv
import logging
import os
import sys
from io import open

from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import matthews_corrcoef, f1_score

logger = logging.getLogger(__name__)


class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text_a, text_b=None, label=None):
        """Constructs a InputExample.

        Args:
            guid: Unique id for the example.
            text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
            text_b: (Optional) string. The untokenized text of the second sequence.
            Only must be specified for sequence pair tasks.
            label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label


class InputFeatures(object):
    """A single set of features of data."""

    def __init__( self, input_ids, input_mask, segment_ids, label_id, epa_vec = None ):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_id = label_id
        self.epa_vec = epa_vec


class DataProcessor(object):
    """Base class for data converters for sequence classification data sets."""

    def get_train_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_dev_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()

    @classmethod
    def _read_tsv(cls, input_file, quotechar=None):
        """Reads a tab separated value file."""
        with open(input_file, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter="\t", quotechar=quotechar)
            lines = []
            for line in reader:
                if sys.version_info[0] == 2:
                    line = list(unicode(cell, 'utf-8') for cell in line)
                lines.append(line)
            return lines


class RelationProcessor( DataProcessor ):
    """Processor for the Relation data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["advise","effect","int","mechanism","NAN"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class SemEval5Processor( DataProcessor ):
    """Processor for the SemEval5 data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["0", "1"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class CironProcessor( DataProcessor ):
    """Processor for the Irony data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["1", "2", "3", "4", "5"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class TwitterProcessor( DataProcessor ):
    """Processor for the Twitter data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["0", "1"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class TrecProcessor( DataProcessor ):
    """Processor for the SST2 data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["0", "1", "2", "3", "4", "5"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class SubjProcessor( DataProcessor ):
    """Processor for the Subjectivity data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["0", "1"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class Ssst2Processor( DataProcessor ):
    """Processor for the SST2 data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["0", "1"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class Spr2018Processor( DataProcessor ):
    """Processor for the Movie review data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["0", "1"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class MrProcessor( DataProcessor ):
    """Processor for the Movie review data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["0", "1"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class LiarProcessor( DataProcessor ):
    """Processor for the Movie review data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["0", "1", "2", "3", "4", "5"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class AirrecordProcessor( DataProcessor ):
    """Processor for the Airrecord data set (EXP version)."""

    def get_train_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "train.tsv" ) ), "train" )

    def get_dev_examples( self, data_dir ):
        """See base class."""
        return self._create_examples( 
            self._read_tsv( os.path.join( data_dir, "dev.tsv" ) ), "dev" )

    def get_labels( self ):
        """See base class."""
        return ["0", "1", "2"]

    def _create_examples( self, lines, set_type ):
        """Creates examples for the training and dev sets."""
        examples = []
        for ( i, line ) in enumerate( lines ):
            if i == 0:
                continue
            guid = "%s-%s" % ( set_type, i )
            try:
                text_a = line[0]
            except:
                print( i )
                print( line )
            try:
                label = line[1]
            except:
                print( i )
                print( line )
            examples.append( 
                InputExample( guid = guid, text_a = text_a, text_b = None, label = label ) )
        return examples


class MrpcProcessor(DataProcessor):
    """Processor for the MRPC data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        logger.info("LOOKING AT {}".format(os.path.join(data_dir, "train.tsv")))
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, i)
            text_a = line[3]
            text_b = line[4]
            label = line[0]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class MnliProcessor(DataProcessor):
    """Processor for the MultiNLI data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev_matched.tsv")),
            "dev_matched")

    def get_labels(self):
        """See base class."""
        return ["contradiction", "entailment", "neutral"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[8]
            text_b = line[9]
            label = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class MnliMismatchedProcessor(MnliProcessor):
    """Processor for the MultiNLI Mismatched data set (GLUE version)."""

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev_mismatched.tsv")),
            "dev_matched")


class ColaProcessor(DataProcessor):
    """Processor for the CoLA data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            guid = "%s-%s" % (set_type, i)
            text_a = line[3]
            label = line[1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
        return examples


class Sst2Processor(DataProcessor):
    """Processor for the SST-2 data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, i)
            text_a = line[0]
            label = line[1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=None, label=label))
        return examples


class StsbProcessor(DataProcessor):
    """Processor for the STS-B data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_labels(self):
        """See base class."""
        return [None]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[7]
            text_b = line[8]
            label = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class QqpProcessor(DataProcessor):
    """Processor for the QQP data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            try:
                text_a = line[3]
                text_b = line[4]
                label = line[5]
            except IndexError:
                continue
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class QnliProcessor(DataProcessor):
    """Processor for the QNLI data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), 
            "dev_matched")

    def get_labels(self):
        """See base class."""
        return ["entailment", "not_entailment"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[1]
            text_b = line[2]
            label = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class RteProcessor(DataProcessor):
    """Processor for the RTE data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_labels(self):
        """See base class."""
        return ["entailment", "not_entailment"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[1]
            text_b = line[2]
            label = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


class WnliProcessor(DataProcessor):
    """Processor for the WNLI data set (GLUE version)."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    def _create_examples(self, lines, set_type):
        """Creates examples for the training and dev sets."""
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            guid = "%s-%s" % (set_type, line[0])
            text_a = line[1]
            text_b = line[2]
            label = line[-1]
            examples.append(
                InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples


def convert_examples_to_features(examples, label_list, max_seq_length,
                                 tokenizer, output_mode,
                                 cls_token_at_end=False,
                                 cls_token='[CLS]',
                                 cls_token_segment_id=1,
                                 sep_token='[SEP]',
                                 sep_token_extra=False,
                                 pad_on_left=False,
                                 pad_token=0,
                                 pad_token_segment_id=0,
                                 sequence_a_segment_id=0, 
                                 sequence_b_segment_id=1,
                                 mask_padding_with_zero = True,
                                 epa_infos = None ):
    """ Loads a data file into a list of `InputBatch`s
        `cls_token_at_end` define the location of the CLS token:
            - False (Default, BERT/XLM pattern): [CLS] + A + [SEP] + B + [SEP]
            - True (XLNet/GPT pattern): A + [SEP] + B + [SEP] + [CLS]
        `cls_token_segment_id` define the segment id associated to the CLS token (0 for BERT, 2 for XLNet)
    """

    label_map = {label : i for i, label in enumerate(label_list)}

    features = []
    for (ex_index, example) in enumerate(examples):
        if ex_index % 10000 == 0:
            logger.info("Writing example %d of %d" % (ex_index, len(examples)))

        tokens_a, epa_vec = tokenizer.tokenize( example.text_a, epa_infos )

        tokens_b = None
        if example.text_b:
            tokens_b = tokenizer.tokenize(example.text_b)
            # Modifies `tokens_a` and `tokens_b` in place so that the total
            # length is less than the specified length.
            # Account for [CLS], [SEP], [SEP] with "- 3". " -4" for RoBERTa.
            special_tokens_count = 4 if sep_token_extra else 3
            _truncate_seq_pair(tokens_a, tokens_b, max_seq_length - special_tokens_count)
        else:
            # Account for [CLS] and [SEP] with "- 2" and with "- 3" for RoBERTa.
            special_tokens_count = 3 if sep_token_extra else 2
            if len(tokens_a) > max_seq_length - special_tokens_count:
                tokens_a = tokens_a[:(max_seq_length - special_tokens_count)]
                epa_vec = epa_vec[:( max_seq_length - special_tokens_count )]

        # The convention in BERT is:
        # (a) For sequence pairs:
        #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
        #  type_ids:   0   0  0    0    0     0       0   0   1  1  1  1   1   1
        # (b) For single sequences:
        #  tokens:   [CLS] the dog is hairy . [SEP]
        #  type_ids:   0   0   0   0  0     0   0
        #
        # Where "type_ids" are used to indicate whether this is the first
        # sequence or the second sequence. The embedding vectors for `type=0` and
        # `type=1` were learned during pre-training and are added to the wordpiece
        # embedding vector (and position vector). This is not *strictly* necessary
        # since the [SEP] token unambiguously separates the sequences, but it makes
        # it easier for the model to learn the concept of sequences.
        #
        # For classification tasks, the first vector (corresponding to [CLS]) is
        # used as as the "sentence vector". Note that this only makes sense because
        # the entire model is fine-tuned.
        tokens = tokens_a + [sep_token]
        epa_vec = epa_vec + [1.0]
        if sep_token_extra:
            # roberta uses an extra separator b/w pairs of sentences
            tokens += [sep_token]
            epa_vec = epa_vec + [1.0]
        segment_ids = [sequence_a_segment_id] * len(tokens)

        if tokens_b:
            tokens += tokens_b + [sep_token]
            segment_ids += [sequence_b_segment_id] * (len(tokens_b) + 1)

        if cls_token_at_end:
            tokens = tokens + [cls_token]
            epa_vec = epa_vec + [1.0]
            segment_ids = segment_ids + [cls_token_segment_id]
        else:
            tokens = [cls_token] + tokens
            epa_vec = [1.0] + epa_vec
            segment_ids = [cls_token_segment_id] + segment_ids

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # The mask has 1 for real tokens and 0 for padding tokens. Only real
        # tokens are attended to.
        input_mask = [1 if mask_padding_with_zero else 0] * len(input_ids)

        # Zero-pad up to the sequence length.
        padding_length = max_seq_length - len(input_ids)
        if pad_on_left:
            input_ids = ([pad_token] * padding_length) + input_ids
            input_mask = ([0 if mask_padding_with_zero else 1] * padding_length) + input_mask
            segment_ids = ([pad_token_segment_id] * padding_length) + segment_ids
            epa_vec = ( [0.0] * padding_length ) + epa_vec
        else:
            input_ids = input_ids + ([pad_token] * padding_length)
            input_mask = input_mask + ([0 if mask_padding_with_zero else 1] * padding_length)
            segment_ids = segment_ids + ([pad_token_segment_id] * padding_length)
            epa_vec = epa_vec + ( [0.0] * padding_length )

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        assert len( epa_vec ) == max_seq_length

        if output_mode == "classification":
            label_id = label_map[example.label]
        elif output_mode == "regression":
            label_id = float(example.label)
        else:
            raise KeyError(output_mode)

        if ex_index < 5:
            logger.info("*** Example ***")
            logger.info("guid: %s" % (example.guid))
            logger.info("tokens: %s" % " ".join(
                    [str(x) for x in tokens]))
            logger.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
            logger.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
            logger.info("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
            logger.info("label: %s (id = %d)" % (example.label, label_id))

        features.append(
                InputFeatures(input_ids=input_ids,
                              input_mask=input_mask,
                              segment_ids=segment_ids,
                              label_id = label_id,
                              epa_vec = epa_vec,
                              ) )
    return features


def _truncate_seq_pair(tokens_a, tokens_b, max_length):
    """Truncates a sequence pair in place to the maximum length."""

    # This is a simple heuristic which will always truncate the longer sequence
    # one token at a time. This makes more sense than truncating an equal percent
    # of tokens from each, since if one sequence is very short then each token
    # that's truncated likely contains more information than a longer sequence.
    while True:
        total_length = len(tokens_a) + len(tokens_b)
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()


def simple_accuracy(preds, labels):
    return (preds == labels).mean()


def acc_and_f1(preds, labels):
    acc = simple_accuracy(preds, labels)
    f1 = f1_score( y_true = labels, y_pred = preds, average = 'macro' )
    print( acc )
    print( '\n' )
    print( f1 )
    print( '\n' )
    return {
        "acc": acc,
        "f1": f1,
        "acc_and_f1": (acc + f1) / 2,
    }


def pearson_and_spearman(preds, labels):
    pearson_corr = pearsonr(preds, labels)[0]
    spearman_corr = spearmanr(preds, labels)[0]
    return {
        "pearson": pearson_corr,
        "spearmanr": spearman_corr,
        "corr": (pearson_corr + spearman_corr) / 2,
    }


def compute_metrics(task_name, preds, labels):
    assert len(preds) == len(labels)
    if task_name == "cola":
        return {"mcc": matthews_corrcoef(labels, preds)}
    elif task_name == "relation":
        return {"acc_and_f1": acc_and_f1( preds, labels )}
    elif task_name == "semeval5":
        return {"acc": simple_accuracy( preds, labels )}
    elif task_name == "ciron":
        return {"acc": simple_accuracy( preds, labels )}
    elif task_name == "sst-2":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "airrecord":
        return {"acc": simple_accuracy( preds, labels )}
    elif task_name == "liar":
        return {"acc": simple_accuracy( preds, labels )}
    elif task_name == "mr":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "spr2018":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "ssst2":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "subj":
        return {"acc": simple_accuracy( preds, labels )}
    elif task_name == "trec":
        return {"acc": simple_accuracy(preds, labels)}   
    elif task_name == "twitter":
        return {"acc": simple_accuracy( preds, labels )}
    elif task_name == "mrpc":
        return acc_and_f1(preds, labels)
    elif task_name == "sts-b":
        return pearson_and_spearman(preds, labels)
    elif task_name == "qqp":
        return acc_and_f1(preds, labels)
    elif task_name == "mnli":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "mnli-mm":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "qnli":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "rte":
        return {"acc": simple_accuracy(preds, labels)}
    elif task_name == "wnli":
        return {"acc": simple_accuracy(preds, labels)}
    else:
        raise KeyError(task_name)

processors = {
    "cola": ColaProcessor,
    "mnli": MnliProcessor,
    "mnli-mm": MnliMismatchedProcessor,
    "relation": RelationProcessor,
    "semeval5": SemEval5Processor,
    "ciron": CironProcessor,
    "mrpc": MrpcProcessor,
    "sst-2": Sst2Processor,
    "airrecord": AirrecordProcessor,
    "liar": LiarProcessor,
    "mr": MrProcessor,
    "spr2018": Spr2018Processor,
    "ssst2": Ssst2Processor,
    "subj": SubjProcessor,
    "trec": TrecProcessor,
    "twitter": TwitterProcessor,
    "sts-b": StsbProcessor,
    "qqp": QqpProcessor,
    "qnli": QnliProcessor,
    "rte": RteProcessor,
    "wnli": WnliProcessor,
}

output_modes = {
    "cola": "classification",
    "mnli": "classification",
    "mnli-mm": "classification",
    "relation": "classification",
    "semeval5": "classification",
    "ciron": "classification",
    "mrpc": "classification",
    "sst-2": "classification",
    "airrecord": "classification",
    "liar": "classification",
    "mr": "classification",
    "spr2018": "classification",
    "ssst2": "classification",
    "subj": "classification",
    "trec": "classification",
    "twitter": "classification",
    "sts-b": "regression",
    "qqp": "classification",
    "qnli": "classification",
    "rte": "classification",
    "wnli": "classification",
}

GLUE_TASKS_NUM_LABELS = {
    "cola": 2,
    "mnli": 3,
    "relation": 5,
    "semeval5": 2,
    "ciron": 5,
    "mrpc": 2,
    "sst-2": 2,
    "airrecord": 3,
    "liar": 6,
    "mr": 2,
    "spr2018": 2,
    "subj": 2,
    "ssst2": 2,
    "trec": 6,
    "twitter": 2,
    "sts-b": 1,
    "qqp": 2,
    "qnli": 2,
    "rte": 2,
    "wnli": 2,
}
