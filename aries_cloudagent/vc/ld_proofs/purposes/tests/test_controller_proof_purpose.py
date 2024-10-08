from datetime import datetime, timedelta
from unittest import IsolatedAsyncioTestCase, mock

from ....tests.data import TEST_VC_DOCUMENT_SIGNED_DID_KEY_ED25519
from ....tests.document_loader import custom_document_loader
from ..controller_proof_purpose import ControllerProofPurpose
from ..proof_purpose import ProofPurpose


class TestControllerProofPurpose(IsolatedAsyncioTestCase):
    async def test_properties(self):
        term = "TestTerm"
        date = datetime.now()
        delta = timedelta(1)
        proof_purpose = ControllerProofPurpose(
            term=term, date=date, max_timestamp_delta=delta
        )
        proof_purpose2 = ControllerProofPurpose(
            term=term, date=date, max_timestamp_delta=delta
        )

        assert proof_purpose.term == term
        assert proof_purpose.date == date
        assert proof_purpose.max_timestamp_delta == delta

        assert proof_purpose2 == proof_purpose
        assert proof_purpose != 10

    async def test_validate(self):
        proof_purpose = ControllerProofPurpose(term="assertionMethod")

        document = TEST_VC_DOCUMENT_SIGNED_DID_KEY_ED25519.copy()
        proof = document.pop("proof")
        suite = mock.MagicMock()
        verification_method = {
            "id": TEST_VC_DOCUMENT_SIGNED_DID_KEY_ED25519["proof"]["verificationMethod"],
            "controller": TEST_VC_DOCUMENT_SIGNED_DID_KEY_ED25519["issuer"],
        }

        result = proof_purpose.validate(
            proof=proof,
            document=document,
            suite=suite,
            verification_method=verification_method,
            document_loader=custom_document_loader,
        )

        assert result.valid

    async def test_validate_controller_invalid_type(self):
        proof_purpose = ControllerProofPurpose(term="assertionMethod")

        document = TEST_VC_DOCUMENT_SIGNED_DID_KEY_ED25519.copy()
        proof = document.pop("proof")
        suite = mock.MagicMock()
        verification_method = {
            "id": TEST_VC_DOCUMENT_SIGNED_DID_KEY_ED25519["proof"]["verificationMethod"],
            "controller": 10,
        }

        result = proof_purpose.validate(
            proof=proof,
            document=document,
            suite=suite,
            verification_method=verification_method,
            document_loader=custom_document_loader,
        )

        assert not result.valid
        assert '"controller" must be a string or dict' in str(result.error)

    async def test_validate_x_not_authorized(self):
        proof_purpose = ControllerProofPurpose(term="assertionMethod")

        document = TEST_VC_DOCUMENT_SIGNED_DID_KEY_ED25519.copy()
        proof = document.pop("proof")
        suite = mock.MagicMock()
        verification_method = {
            "id": TEST_VC_DOCUMENT_SIGNED_DID_KEY_ED25519["proof"]["verificationMethod"],
            "controller": "did:example:489398593",
        }

        result = proof_purpose.validate(
            proof=proof,
            document=document,
            suite=suite,
            verification_method=verification_method,
            document_loader=custom_document_loader,
        )

        assert not result.valid
        assert "not authorized by controller for proof purpose" in str(result.error)

    async def test_validate_x_super_invalid(self):
        proof_purpose = ControllerProofPurpose(term="assertionMethod")

        with mock.patch.object(ProofPurpose, "validate") as validate_mock:
            validate_mock.return_value = mock.MagicMock(valid=False)

            result = proof_purpose.validate(
                proof=mock.MagicMock(),
                document=mock.MagicMock(),
                suite=mock.MagicMock(),
                verification_method=mock.MagicMock(),
                document_loader=mock.MagicMock(),
            )

            assert not result.valid
            assert result == validate_mock.return_value
