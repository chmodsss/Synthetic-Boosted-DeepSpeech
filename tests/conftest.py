import os
import pytest
from typing import List
from keras import Model
from source.configuration import ModelConfiguration
from source.deepspeech import DeepSpeech, Alphabet
from source.generator import DataGenerator
from source.utils import chdir
chdir(to='ROOT')


@pytest.fixture
def test_dir() -> str:
    return 'tests'


@pytest.fixture
def config_path(test_dir) -> str:
    return os.path.join(test_dir, 'models', 'default', 'configuration.yaml')


@pytest.fixture
def alphabet_path(test_dir) -> str:
    return os.path.join(test_dir, 'models', 'default', 'alphabet.txt')


@pytest.fixture
def config(config_path) -> ModelConfiguration:
    return DeepSpeech.get_configuration(config_path)


@pytest.fixture
def alphabet(alphabet_path: str) -> Alphabet:
    return DeepSpeech.get_alphabet(alphabet_path)


@pytest.fixture
def deepspeech(config_path: str, alphabet_path: str) -> DeepSpeech:
    return DeepSpeech.construct(config_path, alphabet_path)


@pytest.fixture
def model(deepspeech: DeepSpeech) -> Model:
    return deepspeech.model


@pytest.fixture
def audio_file_paths() -> List[str]:
    return ['tests/data/audio/sent000.wav', 'tests/data/audio/sent001.wav',
            'tests/data/audio/sent002.wav', 'tests/data/audio/sent003.wav']


@pytest.fixture
def generator(deepspeech: DeepSpeech) -> DataGenerator:
    return DataGenerator.from_audio_files(
        file_path='tests/data/audio.csv',
        alphabet=deepspeech.alphabet,
        features_extractor=deepspeech.features_extractor,
        batch_size=2
    )


@pytest.fixture
def syn_generator(deepspeech: DeepSpeech) -> DataGenerator:
    return DataGenerator.from_audio_files(
        file_path='tests/data/audio.csv',
        alphabet=deepspeech.alphabet,
        features_extractor=deepspeech.features_extractor,
        batch_size=2,
        is_adversarial=True,
        is_synthesized=True
    )
