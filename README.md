# Smart Contract Mutation Testing 


## Table of Contents

- [Setup](#setup)
- [Clone](#clone)
- [Run](#run)

---

## Setup

- install npm

> use `https://www.npmjs.com/get-npm` and make sure `npm` is accessible through command-line

- install truffle

> after installing `npm`, now you can use it to install neccessary packages

```shell
$ npm install -g truffle
```
> then you can run command bellow to check if `truffle` is installed successfully

```shell
$ truffle --version
```

- install python 3.7

> use `https://www.python.org/downloads/`, install python3.7 and make sure `python` is accessible through command-line

- install universal mutator

> use commands below to install universal mutator

```shell
$ npm install -g universalmutator
$ mutate
```

### Clone

- Clone this repo to your local machine using `https://github.com/fvcproductions/SOMEREPO`

### Run

### Setep 1
- before running the project, first you need to make sure your contract is valid with truffle.

> create a truffle project

```shell
$ truffle init
```

> copy your contract into the `contracts` folder and compile the project using command below. make sure your contract is valid.

```shell
$ truffle compile
```

> copy your test net into the `test` folder and run tests. here there is no need to check if tests pass or failed, just check there is no error running the command below

```shell
$ truffle test
```
### Step 2
	- some changes should be done for running the project

	> open project directory `src/contract/` and copy the content of your contract to the `contract.sol`

	> open project directory `src/test/` and copy the content of your test net to the `test.js`

	> open your test net, you see a code like below:

```javascript
	...

contract('KingOfTheEtherThrone', async (accounts) => {
  const maintainer = accounts[0];
  const user1 = accounts[1];
  const user2 = accounts[2];
  const stranger = accounts[3];

  let kingoftheetherthrone;

  beforeEach(async () => {
    kingoftheetherthrone = await KingOfTheEtherThrone.new({from: maintainer});
  });

  ...
```

	> as you see, in test net we define a variable to contain out contract, here it can be seen in `beforeEach` part as `kingoftheetherthrone`. copy this name. then open main in the project directory and place the name you copied in the first line of main as `contract_name`

### Step 3
	> run project using command below:

```shell
$ python main.py
```
