from billing.parametrize import myfunction, requests
import pytest
from unittest.mock import Mock, patch, call


def test_myfunction():
    res = Mock()
    res.status_code = 200
    with patch.object(requests, 'get', side_effect = [res, Exception("Raised from here")]) as patch_response:

        assert "success" == myfunction("dummy")
        assert "Raised" in myfunction("dummy")

        # with pytest.raises(Exception) as e:
        #     myfunction("dummy")


