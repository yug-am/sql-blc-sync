`truffle develop`
`migrate --reset`
setting up

```
var acc = accounts[0];
let instance = await RBMig.deployed()
```

```
await instance.getHash({from:acc})

await instance.createPlotEntry('1','kl_clt_01',true,{from:acc})

await instance.getHash({from:acc})

```