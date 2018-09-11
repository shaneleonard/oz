from oz.config import config, ConfigItem

def test_basic_config():
    # In the shell environment, set the TEST_FAIL or TEST_PASS variables to
    # change the outcome of this test.
    config.register('test_fail', env_key='TEST_FAIL', default=False)
    config.register('test_pass', env_key='TEST_PASS', default=True)

    assert config['test_fail'] == False
    assert config['test_pass'] == True

