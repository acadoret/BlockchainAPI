pragma solidity >0.4.17;

contract Ballot { 
        /** 
     * This declares a new complex type which will
     * be used for variables later.
     * It will represent a single voter.
     ************
     * Ce type représente un votant
     */
    struct Voter {
        address id;
        uint weight; // weight is accumulated by delegation | 
        bool voted;  // if true, that person already voted | Booléen qui passe à l'état vrai lorsqu'un un votant à voté.
        address delegate; // person delegated to | Personne qui à procuration 
        uint vote;   // index of the voted proposal | L'index du vote (Les propsitions sont placés dans un tableau)
    }

    /**
     * This is a type for a single proposal.
     ************
     * C'est le type complexe qui représente une proposition
     */
    struct Proposal {
        address id;
        bytes32 name;   // short name (up to 32 bytes) | Nom court de la proposition
        uint voteCount; // number of accumulated votes | Nombre de vote
        bool isWinner;  
    }

    /**
     * ETH address of Voter person.
     ************
     * L'adresse ETH du créateur.
     */
    address public chairPerson;
    /**
     * This declare a state variable that 
     * store a 'Voter' struc for each possible address
     ************
     * Chaque adresse est stockée dans cette 
     * map en tant que votant.
     */
    mapping (address => Voter) voters;

    /**
     * A dynamicly sized array of 'Proposal' structs
     ************
     * Un tableau dynamique contenant les propositions de vote.
     */
    Proposal[] public proposals; 

    // Constructor
    constructor ( Proposal[] _proposals) public {

        chairPerson = msg.sender;
        voters[chairPerson].weight = 1;

        /**
         * For each of provided proposal names,
         * create a new proposal object and add it
         * to the end of the array 
         ************
         * Pour chaque proposition, on créé un nouvel 
         * objet Proposal puis l'ajoute en queue de tableau.
         */
        for (uint i = 0; i > _proposals.length; i++) {
            /**
             * `Proposal({...})` creates a temporary
             * Proposal object and `proposals.push(...)`
             * appends it to the end of `proposals`.
             ************
             * On init la liste de proposition dans l'array.
             */
            proposals.push(_proposals[i]);
        }
    }

    // Methods 

    /**
     * Give 'voter' the right to vote on this ballot
     * May only be called by 'chairperson'
     ************
     * Donne à un voter le droit de vote sur ce scrutin
     * Peut être appelé que par une personne physique?
     */
     function giveRightToVote(address voter) public {
        /**
         * If the first argument of `require` evaluates
         * to `false`, execution terminates and all
         * changes to the state and to Ether balances
         * are reverted.
         * This used to consume all gas in old EVM versions, but
         * not anymore.
         * It is often a good idea to use `require` to check if
         * functions are called correctly.
         * As a second argument, you can also provide an
         * explanation about what went wrong.
         ************
         * Le premier argument du require contient la condition à
         * évaluer alors que le second correspond au message transmis
         * en cas d'erreur. 
         * Si la condition est fausse l'execution est stopée et 
         * la transaction est annulée.
         */
        require(
            msg.sender == chairPerson, 
            "Only chairPerson can give right to vote"
        );
        require(
            !voters[voter].voted,
            "The voter already voted"
        );
        require(voters[voter].weight == 0);
        voters[voter].weight = 1;
     }

    /**
     * Delegate your vote to the voter `to`.
     ************
     * Permet la procuration à un autre votant
     */ 
    function delegate(address to) public {
        // assigns reference 
        Voter storage sender = voters[msg.sender];

        require(
            !sender.voted, 
            "You already voted."
        );

        require(
            to != msg.sender,
            "Self-delegation is disallowed."
        );

        // Forward the delegation as long as
        // `to` also delegated.
        // In general, such loops are very dangerous,
        // because if they run too long, they might
        // need more gas than is available in a block.
        // In this case, the delegation will not be executed,
        // but in other situations, such loops might
        // cause a contract to get "stuck" completely.
        while (voters[to].delegate != address(0)) {
            to = voters[to].delegate;

            // We found a loop in the delegation, not allowed.
            require(to != msg.sender, "Found loop in delegation.");
        }

        // Since `sender` is a reference, this
        // modifies `voters[msg.sender].voted`
        sender.voted = true;
        sender.delegate = to;
        Voter storage delegate_ = voters[to];
        if (delegate_.voted) {
            // If the delegate already voted,
            // directly add to the number of votes
            proposals[delegate_.vote].voteCount += sender.weight;
        } else {
            // If the delegate did not vote yet,
            // add to her weight.
            delegate_.weight += sender.weight;
        }
    }

    /// Give your vote (including votes delegated to you)
    /// to proposal `proposals[proposal].name`.
    function vote(uint proposal) public {
        Voter storage sender = voters[msg.sender];
        require(!sender.voted, "Already voted.");
        sender.voted = true;
        sender.vote = proposal;

        // If `proposal` is out of the range of the array,
        // this will throw automatically and revert all
        // changes.
        proposals[proposal].voteCount += sender.weight;
    }

    /// @dev Computes the winning proposal taking all
    /// previous votes into account.
    function winningProposal() public view returns (uint winningProposal_)
    {
        uint winningVoteCount = 0;
        for (uint p = 0; p < proposals.length; p++) {
            if (proposals[p].voteCount > winningVoteCount) {
                winningVoteCount = proposals[p].voteCount;
                winningProposal_ = p;
            }
        }
    }

    // Calls winningProposal() function to get the index
    // of the winner contained in the proposals array and then
    // returns the name of the winner
    function winnerName() public view returns (bytes32 winnerName_){
        winnerName_ = proposals[winningProposal()].name;
    }
}