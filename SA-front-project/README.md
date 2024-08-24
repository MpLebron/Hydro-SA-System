# Sensitivity-Analysis-front

> A sensitivity analysis front-end project built with Vue2 + ElementUI
> n Vscode, you need to install the Vuter plugin to parse Vue2 templates. Note that the Volar plugin is not suitable, as it is designed for Vue3
>
> In a broad sense, the SA platform involves many systems within the OpenGMS group, and you can refer to the distributed architecture diagram in the paper.
> In a narrow sense, the SA platform is designed to involve the SA front-end and SA back-end, these two code systems, as well as MongoDB and GeoServer, these two data storage systems.

## Build Setup

```bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# build for production with minification
npm run build

# build for production and view the bundle analyzer report
npm run build --report
```

## Table of Contents

> 2022.05.29

```js
|-- SA-PROJECT
    |-- build
    |-- config
    |   |-- index.js
    |-- src
    |   |-- App.vue
    |   |-- main.js
    |   |-- assets
    |   |-- components
    |       |-- Header.vue
    |       |-- Footer.vue
    |       |-- MapBox.vue
    |   |-- router
    |   |-- views
    |       |-- 1 libraryPage
    |       |-- 2 managePage
    |       |-- 3 modelList
    |       |-- 4 paramCaResult
    |       |-- 5 paramStateSR
    |       |-- 6 dataState
    |       |-- 7 paramState
    |       |-- 8 processStep
    |       |-- 9 saPage
    |       |-- 10 scoreSA
    |       |-- 11 scoreSAQual
    |       |-- 12 simResult
    |       |-- 13 simSetting
    |-- static
    |-- README.md
```

> Tips:
>
> 1. After clicking to start running, you can check the parameter sampling situation in the server's D:\saProjectData.
> 2. You can view the task distribution by looking at the model container (it may take a few minutes to update).
> 3. After the tasks have been successfully run repeatedly, you can check the extraction of results in the server's D:\saProjectData.
>
> During the process, the simulation task may fail due to unknown reasons such as network issues.
>
> 1. The invoke method in the processStep component will re-publish the failed tasks.
> 2. It is necessary to compare the sequence numbers printed in the browser with those in the result summary file to see if they are consistent (this can be directly determined by the number of lines).
> 3. If there is any missing data, you can run the result extraction script on the server and manually add it (the subsequent target function calculation and SA calculation will only proceed once the total number of summary results is correct).
