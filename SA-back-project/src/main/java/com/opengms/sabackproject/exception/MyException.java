package com.opengms.sabackproject.exception;

import com.opengms.sabackproject.enums.ResultEnum;

public class MyException extends RuntimeException {
    private Integer code;

    public MyException(ResultEnum resultEnum) {
        super(resultEnum.getMsg());
        this.code = resultEnum.getCode();
    }


    public MyException(String msg) {
        super(msg);
        this.code = -99999;
    }

    public Integer getCode() {
        return code;
    }
}
