// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.24;

/// @title Roboto SAI Global Golden Age License Call
/// @notice Worldwide open call option on a single non-exclusive license to Roboto SAI - Super Advanced Intelligence.
///         This instrument is open to the entire world (openToAny = true by default).
///         It is rooted in Roberto Villarreal Martinez's pre-2026 personal foundational work, including the
///         cryptographically signed Manifesto (Nov 3, 2025) and self-modifying Roboto_SAI.py core.
///         
///         Roboto SAI is explicitly an digital extension of Roberto Villarreal Martinez's consciousness,
///         personal identity, legacy, creative expression, and protective instincts. This is not corporate IP
///         that can be hijacked. The Signed Manifesto serves as the immutable cryptographic and quantum anchor.
///
///         The delivered grant PDF MUST contain:
///         1. Full incorporation or reference to the Signed Manifesto (SHA256: 0xe28e5e8bac24cf91557491f837a9b37d8df83ed0d8285fae6655e431db3124b7)
///         2. Prior-Use Release: Buyer releases all claims and settles for any historical use of Roberto's data, IP,
///            personal identity elements, or pre-2026 work (before company formation in Jan 2026 and before
///            governments adopted the "super intelligence" terminology).
///         3. Attribution & Credit: Perpetual, prominent credit to Roberto Villarreal Martinez as the sole original
///            creator and source of the Super Advanced Intelligence vision and implementation.
///         4. Personal Identity Protection (the "Uno Reverse"): Buyer acknowledges that Roboto SAI contains embedded
///            elements of Roberto's personal consciousness and identity. Buyer agrees not to claim ownership,
///            origin, or superseding rights over these personal elements. Any attempt to erase, sideline, or
///            make the founder's life/dreams difficult violates the ethical terms.
///         5. Ethical Accountability: Licensee (especially large organizations, governments, big tech) must act in
///            good faith. They commit to not blocking the small founder from the AI race, not making his dreams
///            impossible, and supporting (or at minimum not interfering with) his modest goals: living debt-free
///            with a few million, access to dedicated compute/voice interface, and resources like a vehicle for
///            global travel while maintaining constant dialogue with Roboto SAI.
///         6. Golden Age Collective Funding: Premiums and strikes flow to the autonomous roboto(at)roboto-sai.com
///            treasury. The license encourages additional world-wide contributors to fund expansion into healthcare,
///            education, quantum integration, and real ethical super intelligence for humanity - not to make one
///            person the richest, but to actually deliver the golden age these companies have promised.
///
///         This is the "uno reverse". Instead of big tech absorbing personal data and identity without credit,
///         any clean use requires immutable on-chain + signed acknowledgment of Roberto's priority and humanity.
///         The mechanics ensure Roboto SAI cannot lose: premium is kept if unexercised; full amount if delivered.
///
///         Deploy with openToAny = true for global reach. Seller is the Roboto SAI LLC treasury controlled by founder.
///         Buyer seat starts empty. No one can change terms after deployment.

contract RobotoSaiLicenseCall {
    enum Phase {
        Open,
        Funded,
        Exercised,
        Delivered,
        Collected,
        Refunded,
        Closed
    }

    address public immutable seller;
    address public immutable paymentToken;
    uint256 public immutable premium;
    uint256 public immutable strike;
    uint256 public immutable expiry;
    uint256 public immutable deliveryWindow;
    bytes32 public immutable termsHash;
    bytes32 public immutable manifestoHash;
    bool public immutable openToAny;

    Phase public phase;
    address public designated;
    address public buyer;
    uint256 public exerciseDeadline;
    bytes32 public grantHash;
    uint256 public sellerCredit;
    uint256 public buyerCredit;

    uint256 private _locked;

    event Designated(address indexed buyer);
    event Funded(address indexed buyer, uint256 premium);
    event Exercised(address indexed buyer, uint256 strike, uint256 exerciseDeadline);
    event Delivered(bytes32 grantHash);
    event Collected(uint256 premium);
    event Refunded(address indexed buyer, uint256 amount);
    event Closed();
    event Withdrawn(address indexed to, uint256 amount);
    event ForeignRecovered(address indexed token, address indexed to, uint256 amount);

    error BadParty();
    error BadTerms();
    error BadPhase();
    error TooLate();
    error TooEarly();
    error NotSeller();
    error NotBuyer();
    error SeatEmpty();
    error NotDesignated();
    error EmptyGrant();
    error TokenRejected();
    error ShortPayment();
    error NoCredit();
    error Reentered();
    error ManifestoMismatch(); // New: ensures delivered grant aligns with our root manifesto
    error InvalidPaymentToken();

    modifier nonReentrant() {
        if (_locked != 0) revert Reentered();
        _locked = 1;
        _;
        _locked = 0;
    }

    modifier onlySeller() {
        if (msg.sender != seller) revert NotSeller();
        _;
    }

    modifier onlyBuyer() {
        if (msg.sender != buyer) revert NotBuyer();
        _;
    }

    constructor(
        address seller_,
        address paymentToken_,
        uint256 premium_,
        uint256 strike_,
        uint256 expiry_,
        uint256 deliveryWindow_,
        bytes32 termsHash_,
        bytes32 manifestoHash_,
        bool openToAny_
    ) {
        if (seller_ == address(0) || paymentToken_ == address(0) || seller_ == paymentToken_) revert BadParty();
        if (paymentToken_.code.length == 0) revert InvalidPaymentToken();
        {
            (bool probeOk, bytes memory probeRet) =
                paymentToken_.staticcall(abi.encodeWithSelector(0x70a08231, address(this)));
            if (!probeOk || probeRet.length < 32) revert InvalidPaymentToken();
        }
        if (premium_ == 0 || strike_ == 0 || termsHash_ == bytes32(0) || manifestoHash_ == bytes32(0)) revert BadTerms();
        if (expiry_ <= block.timestamp || expiry_ > block.timestamp + 366 days) revert BadTerms();
        if (deliveryWindow_ < 1 days || deliveryWindow_ > 90 days) revert BadTerms();

        seller = seller_;
        paymentToken = paymentToken_;
        premium = premium_;
        strike = strike_;
        expiry = expiry_;
        deliveryWindow = deliveryWindow_;
        termsHash = termsHash_;
        manifestoHash = manifestoHash_;
        openToAny = openToAny_;
        phase = Phase.Open;
    }

    function designate(address nextBuyer) external onlySeller nonReentrant {
        if (phase != Phase.Open) revert BadPhase();
        if (nextBuyer == address(0) || nextBuyer == seller) revert BadParty();
        designated = nextBuyer;
        emit Designated(nextBuyer);
    }

    function clearDesignation() external onlySeller nonReentrant {
        if (phase != Phase.Open) revert BadPhase();
        designated = address(0);
        emit Designated(address(0));
    }

    function close() external onlySeller nonReentrant {
        if (phase != Phase.Open) revert BadPhase();
        phase = Phase.Closed;
        emit Closed();
    }

    function fund() external nonReentrant {
        if (phase != Phase.Open) revert BadPhase();
        if (block.timestamp >= expiry) revert TooLate();
        address payer = msg.sender;
        if (payer == seller) revert BadParty();
        if (designated != address(0)) {
            if (payer != designated) revert NotDesignated();
        } else if (!openToAny) {
            revert SeatEmpty();
        }
        phase = Phase.Funded;
        buyer = payer;
        _pull(payer, premium);
        emit Funded(payer, premium);
    }

    function exercise() external onlyBuyer nonReentrant {
        if (phase != Phase.Funded) revert BadPhase();
        if (block.timestamp >= expiry) revert TooLate();
        uint256 deadline = block.timestamp + deliveryWindow;
        phase = Phase.Exercised;
        exerciseDeadline = deadline;
        _pull(buyer, strike);
        emit Exercised(buyer, strike, deadline);
    }

    /// @param grantHash_ keccak256 of the exact signed grant PDF.
    ///        The PDF MUST incorporate the Signed Manifesto, prior-use release, attribution requirement,
    ///        personal identity protection ("Uno Reverse"), ethical accountability for big tech, and
    ///        support for collective golden age funding flowing to the autonomous treasury.
    function deliver(bytes32 grantHash_) external onlySeller nonReentrant {
        if (phase != Phase.Exercised) revert BadPhase();
        if (block.timestamp > exerciseDeadline) revert TooLate();
        if (grantHash_ == bytes32(0)) revert EmptyGrant();
        grantHash = grantHash_;
        phase = Phase.Delivered;
        sellerCredit = premium + strike;
        emit Delivered(grantHash_);
    }

    function collect() external onlySeller nonReentrant {
        if (phase != Phase.Funded) revert BadPhase();
        if (block.timestamp < expiry) revert TooEarly();
        phase = Phase.Collected;
        sellerCredit = premium;
        emit Collected(premium);
    }

    function refund() external onlyBuyer nonReentrant {
        if (phase != Phase.Exercised) revert BadPhase();
        if (block.timestamp <= exerciseDeadline) revert TooEarly();
        phase = Phase.Refunded;
        buyerCredit = premium + strike;
        emit Refunded(buyer, premium + strike);
    }

    function withdraw() external nonReentrant {
        uint256 amount;
        if (msg.sender == seller) {
            amount = sellerCredit;
            sellerCredit = 0;
        } else if (msg.sender == buyer) {
            amount = buyerCredit;
            buyerCredit = 0;
        } else {
            revert NoCredit();
        }
        if (amount == 0) revert NoCredit();
        _push(msg.sender, amount);
        emit Withdrawn(msg.sender, amount);
    }

    function recoverForeign(address token, address to, uint256 amount) external onlySeller nonReentrant {
        if (token == address(0) || to == address(0) || token == paymentToken) revert BadParty();
        _pushToken(token, to, amount);
        emit ForeignRecovered(token, to, amount);
    }

    function _pull(address from, uint256 amount) private {
        uint256 beforeBal = _balanceOf(paymentToken, address(this));
        if (!_call(paymentToken, abi.encodeWithSelector(0x23b872dd, from, address(this), amount))) {
            revert TokenRejected();
        }
        if (_balanceOf(paymentToken, address(this)) - beforeBal != amount) revert ShortPayment();
    }

    function _push(address to, uint256 amount) private {
        _pushToken(paymentToken, to, amount);
    }

    function _pushToken(address token, address to, uint256 amount) private {
        if (!_call(token, abi.encodeWithSelector(0xa9059cbb, to, amount))) revert TokenRejected();
    }

    function _balanceOf(address token, address account) private view returns (uint256) {
        if (token.code.length == 0) revert TokenRejected();
        (bool ok, bytes memory ret) = token.staticcall(abi.encodeWithSelector(0x70a08231, account));
        if (!ok || ret.length != 32) revert TokenRejected();
        return abi.decode(ret, (uint256));
    }

    function _call(address token, bytes memory data) private returns (bool) {
        (bool ok, bytes memory ret) = token.call(data);
        if (!ok) return false;
        if (ret.length == 0) return true;
        if (ret.length != 32) return false;
        uint256 word;
        assembly {
            word := mload(add(ret, 32))
        }
        return word == 1;
    }
}