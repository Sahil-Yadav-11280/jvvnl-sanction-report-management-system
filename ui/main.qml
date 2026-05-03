import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    Text {
        text: "UI Loaded Successfully"
    }
    visible: true
    width: 600
    height: 800
    title: "Report Manager"

    StackView {
        id: stack
        anchors.fill: parent
        initialItem: homePage
    }

    Component {
        id: homePage

        Column {
            anchors.centerIn: parent
            spacing: 20

            Button {
                text: "New"
                onClicked: stack.push(newPage)
            }

            Button {
                text: "View"
            }
        }
    }

    Component {
        id: newPage

        Flickable {
            anchors.fill: parent
            contentHeight: column.height

            ColumnLayout {
                id: column
                width: parent.width
                spacing: 12
                padding: 20

                TextField {
                    id: purpose
                    placeholderText: "Purpose"
                }

                // 📅 Date Picker
                DatePicker {
                    id: date
                }

                TextField {
                    id: name
                    placeholderText: "Customer Name"
                }

                TextField {
                    id: address
                    placeholderText: "Address"
                }

                TextField {
                    id: sanction_no
                    placeholderText: "Sanction Number"
                }

                // 📅 Sanction Date
                DatePicker {
                    id: sanction_date
                }

                TextField {
                    id: consumer_no
                    placeholderText: "Consumer Number"
                }

                // 🔽 Dropdown for JEN
                ComboBox {
                    id: jen
                    model: ["A", "B", "C", "D"]
                }

                TextArea {
                    id: work
                    placeholderText: "Proposed Work"
                    Layout.preferredHeight: 100
                }

                TextField {
                    id: receipt_no
                    placeholderText: "Demand Deposit Receipt Number"
                }

                // 📅 Receipt Date
                DatePicker {
                    id: receipt_date
                }

                Button {
                    text: "Submit"

                    onClicked: {
                        backend.submit_form(
                            purpose.text,
                            date.date.toString("yyyy-MM-dd"),
                            name.text,
                            address.text,
                            sanction_no.text,
                            sanction_date.date.toString("yyyy-MM-dd"),
                            consumer_no.text,
                            jen.currentText,
                            work.text,
                            receipt_no.text,
                            receipt_date.date.toString("yyyy-MM-dd")
                        )
                    }
                }
            }
        }
    }
}